import pytest
import pandas as pd
from src.features.feature_pipeline import FeatureEngineer


@pytest.fixture
def sample_df():
    """
    Create a sample dataframe for testing.
    """
    data = {
        "tpep_pickup_datetime": ["2022-01-01 08:00:00", "2022-01-01 09:00:00"],
        "tpep_dropoff_datetime": ["2022-01-01 08:30:00", "2022-01-01 09:30:00"],
        "Airport_fee": [1.5, 2.0],
        "PULocationID": [1, 2],
        "DOLocationID": [3, 4],
        "trip_distance": [2.5, 3.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def feature_engineer():
    return FeatureEngineer()


def test_clean_and_engineer(sample_df, feature_engineer):
    """
    Test the _clean_and_engineer method in FeatureEngineer using real data.
    """
    df = feature_engineer._clean_and_engineer(sample_df)
    assert df.shape[0] == 2  # Ensure rows are not dropped unnecessarily
    assert "duration" in df.columns  # Ensure duration column is added
    assert df["PU_DO"].iloc[0] == "1_3"  # Check PU_DO column is correctly created



def test_missing_airport_fee(sample_df, feature_engineer):
    """
    Test that rows with missing airport fees are dropped in the feature engineering pipeline.
    """
    sample_df_with_missing_fee = sample_df.copy()
    sample_df_with_missing_fee.loc[0, "Airport_fee"] = None

    df = feature_engineer._clean_and_engineer(sample_df_with_missing_fee)

    assert df.shape[0] == 1


def test_invalid_duration(sample_df, feature_engineer):
    """
    Test that trips with invalid durations are filtered out in the feature engineering pipeline.
    """
    sample_df_invalid_duration = sample_df.copy()
    sample_df_invalid_duration.loc[0, "tpep_pickup_datetime"] = "2022-01-01 08:00:00"
    sample_df_invalid_duration.loc[0, "tpep_dropoff_datetime"] = "2022-01-01 07:00:00"  # Invalid duration

    df = feature_engineer._clean_and_engineer(sample_df_invalid_duration)

    assert df.shape[0] == 1


@pytest.fixture
def new_data():
    """
    A new sample dataset for inference or transformation tests.
    """
    return {
        "PULocationID": ["186"],
        "DOLocationID": ["79"],
        "trip_distance": ["4"]
    }


# def test_fit_transform(sample_df, feature_engineer):
#     """
#     Test the fit_transform method in FeatureEngineer using real data.
#     """
#     X, y = feature_engineer.fit_transform(sample_df)

#     # Check that fit_transform returns the correct output shapes
#     assert X.shape[0] == 2  # Two rows of data should be transformed
#     assert y.shape[0] == 2  # Two target values should be present


# def test_transform(sample_df, feature_engineer):
#     """
#     Test the transform method in FeatureEngineer using real data.
#     """
#     # First, fit the model to create the DictVectorizer
#     feature_engineer.fit_transform(sample_df)

#     # Now, transform new data
#     df = pd.DataFrame({
#         "Airport_fee": [4.0],
#         "PULocationID": [1],
#         "DOLocationID": [3],
#         "trip_distance": [2.0],
#     })
#     X, y = feature_engineer.transform(df)

#     # Check the transformed data shape
#     assert X.shape[0] == 1  # One row of transformed data
#     assert y.shape[0] == 1  # One target value


# def test_inference(sample_df, feature_engineer):
#     """
#     Test the inference method in FeatureEngineer using real data.
#     """
#     # First, fit the model to create the DictVectorizer
#     feature_engineer.fit_transform(sample_df)

#     # Now, do inference with new data
#     df = pd.DataFrame({
#         "PULocationID": [1],
#         "DOLocationID": [3],
#         "trip_distance": [2.5],
#     })
#     X = feature_engineer.inference(df)

#     # Check the inference result
#     assert X.shape[0] == 1  # One row of data should be returned


# def test_invalid_dict_vectorizer_loading(sample_df, feature_engineer):
#     """
#     Test that the feature engineer raises an error when the DictVectorizer is not found.
#     """
#     feature_engineer.dv = None  # Make sure the vectorizer is not loaded

#     with pytest.raises(ValueError):
#         feature_engineer.transform(sample_df)

# def test_new_data_inference(new_data, feature_engineer):
#     """
#     Test that new data can be processed for inference.
#     """
#     # Fit the model first to create the DictVectorizer
#     feature_engineer.fit_transform(pd.DataFrame({
#         "tpep_pickup_datetime": ["2022-01-01 08:00:00"],
#         "tpep_dropoff_datetime": ["2022-01-01 08:30:00"],
#         "Airport_fee": [1.5],
#         "PULocationID": [1],
#         "DOLocationID": [3],
#         "trip_distance": [2.5],
#     }))

#     # Create the new data DataFrame
#     df = pd.DataFrame(new_data)

#     # Run inference
#     X = feature_engineer.inference(df)

#     # Check that the output has the correct number of rows
#     assert X.shape[0] == 1  # Only one row in the new data

#     # Optionally check if the feature vectorization worked as expected
#     assert X is not None  # Ensure that inference returns a valid result

