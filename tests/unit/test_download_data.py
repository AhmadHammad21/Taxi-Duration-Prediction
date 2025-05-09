import pytest
from pathlib import Path
import pandas as pd
from src.config.settings import AppSettings
from src.data_pulling.download_data import DataDownloader
import tempfile
import os

# Fixture to initialize the downloader with real settings
@pytest.fixture
def mock_settings():
    mock = AppSettings()
    mock.RAW_DATA_DIRECTORY = "/mock/raw_data"
    mock.DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year_month}.parquet"
    mock.TRAINING_DATA_DATE = {"start": "2022-01", "end": "2022-03"}
    mock.TESTING_DATA_DATE = {"start": "2022-04", "end": "2022-06"}
    return mock

# Fixture to initialize the downloader instance
@pytest.fixture
def downloader(mock_settings):
    return DataDownloader(settings=mock_settings)

# Test for generate_month_range
def test_generate_month_range(downloader):
    assert downloader.generate_month_range("2022-01", "2022-01") == ["2022-01"]
    assert downloader.generate_month_range("2022-01", "2022-03") == ["2022-01", "2022-02", "2022-03"]

# Test for download_and_save_parquet_file (downloading one month)
def test_download_and_save_parquet_file(downloader):
    # Use a temporary directory to avoid file system conflicts
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Download the file for January 2022
        file_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"
        downloader.download_and_save_parquet_file(file_url, tmp_path)

        # Verify that the file has been saved
        downloaded_file = tmp_path / "yellow_tripdata_2022-01.parquet"
        assert downloaded_file.exists()

        # Load the parquet file to verify the data (this is a placeholder check)
        df = pd.read_parquet(downloaded_file)
        assert not df.empty  # Verify that the dataframe is not empty

# Test for download_split (downloading one month)
def test_download_split(downloader):
    # Use a temporary directory to avoid file system conflicts
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Perform download for only January 2022
        downloader.download_split("2022-01", "2022-01", tmp_path)

        # Verify that the file for January 2022 is downloaded
        file_path = tmp_path / "yellow_tripdata_2022-01.parquet"
        assert file_path.exists()

# Test for download_all (downloading one month for both train and test)
def test_download_all(downloader):
    # Use a temporary directory to avoid file system conflicts
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create directories for train and test
        train_path = tmp_path / "train"
        test_path = tmp_path / "test"
        train_path.mkdir(parents=True, exist_ok=True)
        test_path.mkdir(parents=True, exist_ok=True)

        # Perform download for one month in the training period (January 2022)
        downloader.download_split("2022-01", "2022-01", train_path)

        # Perform download for one month in the testing period (April 2022)
        downloader.download_split("2022-04", "2022-04", test_path)

        # Verify that the file for January 2022 in the training set is downloaded
        train_file_path = train_path / "yellow_tripdata_2022-01.parquet"
        assert train_file_path.exists()

        # Verify that the file for April 2022 in the testing set is downloaded
        test_file_path = test_path / "yellow_tripdata_2022-04.parquet"
        assert test_file_path.exists()
