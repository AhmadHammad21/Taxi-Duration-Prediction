import pandas as pd
from src.config.settings import settings
from pathlib import Path
import os


def load_and_concat_parquet_files(folder_path: Path) -> pd.DataFrame:
    dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith(".parquet"):
            full_path = folder_path / file
            df = pd.read_parquet(full_path)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

