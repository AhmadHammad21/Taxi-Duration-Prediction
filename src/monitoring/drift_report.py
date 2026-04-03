"""
Drift detection script using Evidently.

Compares the distribution of recent prediction inputs against the training
data (reference). Run this manually or on a schedule.

Usage:
    uv run python -m src.monitoring.drift_report
"""
import sys
from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from loguru import logger

TRAIN_DIR = Path("data/raw/train")
PREDICTIONS_LOG = Path("data/predictions/predictions.csv")
REPORTS_DIR = Path("reports")
FEATURES = ["PULocationID", "DOLocationID", "trip_distance"]
REFERENCE_SAMPLE_SIZE = 10_000
MIN_CURRENT_ROWS = 50


def load_reference() -> pd.DataFrame:
    files = list(TRAIN_DIR.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {TRAIN_DIR}")

    df = pd.concat([pd.read_parquet(f, columns=FEATURES) for f in files], ignore_index=True)
    df = df.dropna(subset=FEATURES)
    df["PULocationID"] = df["PULocationID"].astype(int)
    df["DOLocationID"] = df["DOLocationID"].astype(int)

    if len(df) > REFERENCE_SAMPLE_SIZE:
        df = df.sample(n=REFERENCE_SAMPLE_SIZE, random_state=42)

    logger.info(f"Reference data loaded: {len(df)} rows from {len(files)} file(s)")
    return df.reset_index(drop=True)


def load_current() -> pd.DataFrame:
    if not PREDICTIONS_LOG.exists():
        raise FileNotFoundError(
            f"Predictions log not found at {PREDICTIONS_LOG}. "
            "Make sure the API has received some requests first."
        )

    df = pd.read_csv(PREDICTIONS_LOG)
    df = df[FEATURES].dropna()
    df["PULocationID"] = df["PULocationID"].astype(int)
    df["DOLocationID"] = df["DOLocationID"].astype(int)

    logger.info(f"Current data loaded: {len(df)} rows from prediction log")
    return df.reset_index(drop=True)


def run_drift_report() -> Path:
    reference = load_reference()
    current = load_current()

    if len(current) < MIN_CURRENT_ROWS:
        logger.warning(
            f"Only {len(current)} predictions logged — need at least {MIN_CURRENT_ROWS} "
            "for a meaningful drift report. Send more requests and try again."
        )
        sys.exit(1)

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)

    REPORTS_DIR.mkdir(exist_ok=True)
    output_path = REPORTS_DIR / "drift_report.html"
    report.save_html(str(output_path))
    logger.info(f"Drift report saved to {output_path}")
    return output_path


if __name__ == "__main__":
    run_drift_report()
