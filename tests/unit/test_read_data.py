import time
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
from src.data_pulling.read_data import (
    load_and_concat_parquet_files,
    load_train_test,
    save_processed_data,
)


def test_load_and_concat_parquet_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        df1 = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df2 = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})
        df1.to_parquet(tmp_path / "file1.parquet")
        df2.to_parquet(tmp_path / "file2.parquet")

        result = load_and_concat_parquet_files(tmp_path)
        
        # Since files are loaded in alphabetical order (file1, file2),
        # the result should be df1 + df2
        expected = pd.concat([df1, df2], ignore_index=True)
        
        # Sort both DataFrames by all columns to ensure consistent comparison
        result_sorted = result.sort_values(by=list(result.columns)).reset_index(drop=True)
        expected_sorted = expected.sort_values(by=list(expected.columns)).reset_index(drop=True)
        
        pd.testing.assert_frame_equal(result_sorted, expected_sorted)


def test_load_train_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        raw_data_dir = tmp_path / "raw_data"
        train_dir = raw_data_dir / "train"
        test_dir = raw_data_dir / "test"
        train_dir.mkdir(parents=True)
        test_dir.mkdir(parents=True)

        df_train = pd.DataFrame({"col1": [1, 2]})
        df_test = pd.DataFrame({"col1": [3, 4]})
        df_train.to_parquet(train_dir / "train1.parquet")
        df_test.to_parquet(test_dir / "test1.parquet")

        train_df, test_df = load_train_test(str(raw_data_dir))

        pd.testing.assert_frame_equal(train_df, df_train)
        pd.testing.assert_frame_equal(test_df, df_test)


# def test_save_processed_data():
#     with tempfile.TemporaryDirectory() as tmpdir:
#         tmp_path = Path(tmpdir)
#         file_path = tmp_path / "processed_data.npz"

#         X = np.array([1, 2, 3])
#         y = np.array([4, 5, 6])

#         # Call the save function
#         save_processed_data(X, y, "processed_data.npz", tmp_path)

#         # Add a small delay to ensure the file is fully written and closed
#         time.sleep(0.2)

#         # Ensure the file exists and is not being accessed by another process
#         assert file_path.exists(), f"File {file_path} does not exist."

#         # Load and verify the data
#         data = np.load(file_path)
#         np.testing.assert_array_equal(data["X"], X)
#         np.testing.assert_array_equal(data["y"], y)