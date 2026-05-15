#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import settings


MIN_TRIP_DISTANCE = 0
MAX_TRIP_DISTANCE = 100
REQUIRED_COLUMNS = ["PULocationID", "DOLocationID", "trip_distance"]


def load_training_distances(raw_train_dir: Path) -> pd.DataFrame:
    dataframes = []
    for parquet_path in sorted(raw_train_dir.glob("*.parquet")):
        dataframes.append(pd.read_parquet(parquet_path, columns=REQUIRED_COLUMNS))

    if not dataframes:
        raise FileNotFoundError(f"No parquet files found in {raw_train_dir}")

    return pd.concat(dataframes, ignore_index=True)


def build_distance_lookup(
    raw_train_dir: Path = Path(settings.RAW_DATA_DIRECTORY) / "train",
    output_path: Path = Path(settings.DISTANCE_LOOKUP_PATH),
) -> None:
    df = load_training_distances(raw_train_dir)
    df = df.dropna(subset=REQUIRED_COLUMNS).copy()
    df["trip_distance"] = pd.to_numeric(df["trip_distance"], errors="coerce")
    df = df[
        (df["trip_distance"] > MIN_TRIP_DISTANCE)
        & (df["trip_distance"] <= MAX_TRIP_DISTANCE)
    ].copy()

    df["PU_DO"] = (
        df["PULocationID"].astype("int64").astype(str)
        + "_"
        + df["DOLocationID"].astype("int64").astype(str)
    )

    pair_medians = df.groupby("PU_DO")["trip_distance"].median().round(3)
    lookup = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_directory": str(raw_train_dir),
            "rows_used": int(len(df)),
            "unique_pairs": int(pair_medians.shape[0]),
            "min_trip_distance": MIN_TRIP_DISTANCE,
            "max_trip_distance": MAX_TRIP_DISTANCE,
        },
        "global_median_trip_distance": round(float(df["trip_distance"].median()), 3),
        "global_mean_trip_distance": round(float(df["trip_distance"].mean()), 3),
        "pair_median_trip_distance": pair_medians.to_dict(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(lookup, file, indent=2)

    print(
        f"Saved {len(pair_medians)} pair distance estimates to {output_path} "
        f"using {len(df)} rows"
    )


if __name__ == "__main__":
    build_distance_lookup()