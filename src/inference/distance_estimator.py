import json
from pathlib import Path

from loguru import logger

from ..config.settings import settings


class DistanceEstimator:
    """Estimate trip distance from historical pickup/dropoff zone medians."""

    def __init__(self, lookup_path: str = settings.DISTANCE_LOOKUP_PATH):
        self.lookup_path = Path(lookup_path)
        self.global_distance = settings.DEFAULT_TRIP_DISTANCE
        self.pair_distances: dict[str, float] = {}
        self._load_lookup()

    def _load_lookup(self) -> None:
        if not self.lookup_path.exists():
            logger.warning(
                f"Distance lookup not found at {self.lookup_path}; "
                f"using default distance {self.global_distance}"
            )
            return

        with self.lookup_path.open("r", encoding="utf-8") as file:
            lookup = json.load(file)

        self.global_distance = float(
            lookup.get("global_median_trip_distance", self.global_distance)
        )
        self.pair_distances = {
            key: float(value)
            for key, value in lookup.get("pair_median_trip_distance", {}).items()
        }
        logger.info(
            f"Loaded {len(self.pair_distances)} historical trip distance estimates "
            f"from {self.lookup_path}"
        )

    @staticmethod
    def _pair_key(pu_location_id: str, do_location_id: str) -> str:
        return f"{pu_location_id}_{do_location_id}"

    def estimate(self, pu_location_id: str, do_location_id: str) -> float:
        pair_key = self._pair_key(pu_location_id, do_location_id)
        if pair_key in self.pair_distances:
            return self.pair_distances[pair_key]

        reverse_pair_key = self._pair_key(do_location_id, pu_location_id)
        if reverse_pair_key in self.pair_distances:
            return self.pair_distances[reverse_pair_key]

        return self.global_distance