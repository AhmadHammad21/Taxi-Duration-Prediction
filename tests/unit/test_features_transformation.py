import os
import pytest
import pandas as pd
from src.features.feature_pipeline import FeatureEngineer

@pytest.fixture
def sample_df():
    # Sample DataFrame to test with
    return pd.DataFrame({
        "tpep_pickup_datetime": ["2022-01-01 08:00:00", "2022-01-01 08:30:00"],
        "tpep_dropoff_datetime": ["2022-01-01 08:15:00", "2022-01-01 08:45:00"],
        "Airport_fee": [1.5, 2.0],
        "PULocationID": [1, 2],
        "DOLocationID": [3, 4],
        "trip_distance": [2.5, 3.0],
    })

@pytest.fixture
def new_data():
    # Sample DataFrame to test with
    return pd.DataFrame({
        "tpep_pickup_datetime": ["2022-01-01 08:00:00"],
        "tpep_dropoff_datetime": ["2022-01-01 08:15:00"],
        "Airport_fee": [1.5],
        "PULocationID": [1],
        "DOLocationID": [3],
        "trip_distance": [2.5],
    })

@pytest.fixture
def feature_engineer(tmp_path, sample_df):
    # Create a temporary file path for the DictVectorizer for each test
    dv_path = tmp_path / "test_dict_vectorizer.pkl"

    # Initialize the FeatureEngineer with the temporary path
    feature_engineer = FeatureEngineer(dv_path=str(dv_path))

    # Return the feature engineer instance
    yield feature_engineer

    # Finalize: Remove the temporary file after the test
    if os.path.exists(dv_path):
        os.remove(dv_path)

def test_fit_transform(sample_df, feature_engineer):
    """
    Test the fit_transform method in FeatureEngineer using real data.
    """
    X, y = feature_engineer.fit_transform(sample_df)

    # Check that fit_transform returns the correct output shapes
    assert X.shape[0] == 2  # Two rows of data should be transformed
    assert y.shape[0] == 2  # Two target values should be present

def test_transform(sample_df, feature_engineer):
    """
    Test the transform method in FeatureEngineer using real data.
    """
    # First, fit the model to create the DictVectorizer
    feature_engineer.fit_transform(sample_df)

    # Now, transform new data
    df = pd.DataFrame({
        "tpep_pickup_datetime": ["2022-01-01 08:00:00"],
        "tpep_dropoff_datetime": ["2022-01-01 08:15:00"],
        "Airport_fee": [4.0],
        "PULocationID": [1],
        "DOLocationID": [3],
        "trip_distance": [2.0],
    })
    X, y = feature_engineer.transform(df)

    # Check the transformed data shape
    assert X.shape[0] == 1  # One row of transformed data
    assert y.shape[0] == 1  # One target value

def test_inference(sample_df, feature_engineer):
    """
    Test the inference method in FeatureEngineer using real data.
    """
    # First, fit the model to create the DictVectorizer
    feature_engineer.fit_transform(sample_df)

    # Now, do inference with new data
    df = pd.DataFrame({
        "PULocationID": [1],
        "DOLocationID": [3],
        "trip_distance": [2.5],
    })
    X = feature_engineer.inference(df)

    # Check the inference result
    assert X.shape[0] == 1  # One row of data should be returned

def test_new_data_inference(new_data, feature_engineer):
    """
    Test that new data can be processed for inference.
    """
    # Fit the model first to create the DictVectorizer
    feature_engineer.fit_transform(pd.DataFrame({
        "tpep_pickup_datetime": ["2022-01-01 08:00:00"],
        "tpep_dropoff_datetime": ["2022-01-01 08:30:00"],
        "Airport_fee": [1.5],
        "PULocationID": [1],
        "DOLocationID": [3],
        "trip_distance": [2.5],
    }))

    # Create the new data DataFrame
    df = pd.DataFrame(new_data)

    # Run inference
    X = feature_engineer.inference(df)

    # Check that the output has the correct number of rows
    assert X.shape[0] == 1  # Only one row in the new data

    # Optionally check if the feature vectorization worked as expected
    assert X is not None  # Ensure that inference returns a valid result