import mlflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import numpy as np

def log_regression_metrics_run(y_true, predictions, prefix="test", n_features=None):
    """
    Logs multiple regression metrics for the current MLflow run.
    
    Args:
    y_true (array-like): True target values.
    predictions (array-like): Predicted target values.
    prefix (str): Prefix for the metric name (e.g., 'train', 'test').
    n_features (int): Number of features used in the model (required for Adjusted R2).
    """
    # Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_true, predictions)

    # Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mean_squared_error(y_true, predictions))

    # Mean Absolute Percentage Error (MAPE)
    mape = mean_absolute_percentage_error(y_true, predictions)

    # R-squared (R2)
    r2 = r2_score(y_true, predictions)

    # Adjusted R-squared (Adjusted R2)
    if n_features is not None:
        n_samples = len(y_true)
        adj_r2 = 1 - (1 - r2) * (n_samples - 1) / (n_samples - n_features - 1)
    else:
        adj_r2 = None  # Adjusted R2 requires number of features
    
    # Log metrics to MLflow
    mlflow.log_metric(f"{prefix}_mean_absolute_error", mae)
    mlflow.log_metric(f"{prefix}_root_mean_squared_error", rmse)
    mlflow.log_metric(f"{prefix}_mean_absolute_percentage_error", mape)
    mlflow.log_metric(f"{prefix}_r2", r2)
    
    # Log adjusted R2 if n_features is provided
    if adj_r2 is not None:
        mlflow.log_metric(f"{prefix}_adjusted_r2", adj_r2)