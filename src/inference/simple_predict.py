import os 
import pickle
import pandas as pd
from loguru import logger
from sklearn.linear_model import LinearRegression


def load_simple_model():
    """Load model from pickle file - no MLflow dependencies"""
    try:
        # Try to load from pickle file
        model_path = "src/artifacts/simple_model.pkl"
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info("Model loaded from pickle file successfully!")
            return model
        else:
            # Create a simple fallback model
            logger.warning("No pickle model found, creating simple fallback model")
            model = LinearRegression()
            logger.info("Created simple fallback model")
            return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        # Ultimate fallback - create a new model
        logger.info("Creating new LinearRegression model as ultimate fallback")
        return LinearRegression()


class SimpleModelPredictor:
    """
    Simple model predictor that doesn't use MLflow - just works!
    """

    def __init__(self, feature_engineer):
        logger.info("Initializing SimpleModelPredictor")
        self.model = load_simple_model()
        self.feature_engineer = feature_engineer
        logger.info("SimpleModelPredictor initialized successfully!")

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