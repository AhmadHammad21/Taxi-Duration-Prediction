import pandas as pd
from pathlib import Path
import os
import numpy as np
from loguru import logger


def load_and_concat_parquet_files(folder_path: Path) -> pd.DataFrame:
    dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith(".parquet"):
            full_path = folder_path / file
            df = pd.read_parquet(full_path)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)


def load_train_test(raw_data_directory: str):
    train_data = Path(raw_data_directory) / "train"
    test_data = Path(raw_data_directory) / "test"

    train_df = load_and_concat_parquet_files(train_data)
    test_df = load_and_concat_parquet_files(test_data)

    return train_df, test_df

def save_processed_data(X, y,
                      filename: str,
                      output_dir: Path):

    output_path = output_dir / filename

    np.savez_compressed(output_path, X=X, y=y)
    logger.info(f"✅ Saved processed data to {output_path}")


def load_processed_data(filename: str, output_dir: Path):
    input_path = output_dir / filename
    data = np.load(input_path)
    
    X = data["X"]
    y = data["y"]
    
    logger.info(f"📥 Loaded processed data from {input_path}")

    #X_train, y_train = load_processed_data("train_processed.npz", output_dir)
    return X, y
