import json

from src.inference.distance_estimator import DistanceEstimator


def write_lookup(tmp_path):
    lookup_path = tmp_path / "distance_lookup.json"
    lookup_path.write_text(
        json.dumps(
            {
                "global_median_trip_distance": 1.7,
                "pair_median_trip_distance": {
                    "132_161": 17.25,
                    "186_79": 2.4,
                },
            }
        ),
        encoding="utf-8",
    )
    return lookup_path


def test_estimate_uses_pair_median(tmp_path):
    estimator = DistanceEstimator(lookup_path=str(write_lookup(tmp_path)))

    distance = estimator.estimate("132", "161")

    assert distance == 17.25


def test_estimate_uses_reverse_pair_when_direct_pair_missing(tmp_path):
    estimator = DistanceEstimator(lookup_path=str(write_lookup(tmp_path)))

    distance = estimator.estimate("161", "132")

    assert distance == 17.25


def test_estimate_uses_global_median_when_pair_missing(tmp_path):
    estimator = DistanceEstimator(lookup_path=str(write_lookup(tmp_path)))

    distance = estimator.estimate("1", "999")

    assert distance == 1.7