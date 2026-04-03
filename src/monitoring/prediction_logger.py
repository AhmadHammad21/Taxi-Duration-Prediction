import csv
from pathlib import Path
from datetime import datetime, timezone

PREDICTIONS_LOG = Path("data/predictions/predictions.csv")
COLUMNS = ["timestamp", "PULocationID", "DOLocationID", "trip_distance", "predicted_duration"]


def log_prediction(pu_id: str, do_id: str, trip_distance: float, predicted_duration: float) -> None:
    PREDICTIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    write_header = not PREDICTIONS_LOG.exists()
    with open(PREDICTIONS_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(COLUMNS)
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            int(pu_id),
            int(do_id),
            trip_distance,
            predicted_duration,
        ])
