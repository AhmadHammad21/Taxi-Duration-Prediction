import pandas as pd
from src.inference.predict import ModelPredictor
from src.features.feature_pipeline import FeatureEngineer


def test_model_predictor_valid_input():

    feature_engineer = FeatureEngineer()
    model_predictor = ModelPredictor(feature_engineer=feature_engineer)

    # Test data
    new_data = {
        "PULocationID": ["186"],
        "DOLocationID": ["79"],
        "trip_distance": ["4"]
    }
    new_data_df = pd.DataFrame(new_data)

    predictions = model_predictor.predict(new_data_df)

    # Assertions
    assert predictions is not None
    assert isinstance(predictions, list)
    assert all(isinstance(p, float) for p in predictions)


def test_model_predictor_invalid_input():
    feature_engineer = FeatureEngineer()
    model_predictor = ModelPredictor(feature_engineer=feature_engineer)

    new_data = {
        "invalid_field": ["123"]
    }
    new_data_df = pd.DataFrame(new_data)

    try:
        model_predictor.predict(new_data_df)
        assert False, "Expected an exception due to invalid input"
    except Exception as e:
        assert isinstance(e, Exception)

