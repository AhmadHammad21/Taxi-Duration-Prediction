from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

PREDICTION_VALUE = Histogram(
    "prediction_duration_minutes",
    "Predicted taxi trip duration in minutes",
    buckets=[1, 2, 5, 10, 15, 20, 30, 45, 60, 90, 120],
)

PREDICTION_ERRORS_TOTAL = Counter(
    "prediction_errors_total",
    "Total prediction errors",
    ["endpoint"],
)
