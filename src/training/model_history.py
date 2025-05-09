import mlflow
import pandas as pd
from mlflow import MlflowClient
from typing import Dict, Any
import json

class ModelHistory:
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.client = MlflowClient()
        self.experiment_id = self._get_experiment_id()

    def _get_experiment_id(self) -> str:
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        if not experiment:
            raise ValueError(f"Experiment '{self.experiment_name}' not found.")
        return experiment.experiment_id

    def list_all_runs(self) -> pd.DataFrame:
        """
        List all runs for the given experiment, with relevant metrics.
        """
        runs = self.client.search_runs(self.experiment_id, filter_string="",
                                       run_view_type=mlflow.entities.ViewType.ALL)
        
        # Create a dataframe with run data
        run_data = []
        for run in runs:
            run_info = run.info
            metrics = run.data.metrics
            run_data.append({
                "run_id": run_info.run_id,
                "model_name": run_info.run_name,
                "status": run_info.status,
                "start_time": run_info.start_time,
                "end_time": run_info.end_time,
                "test_mean_absolute_error": metrics.get("test_mean_absolute_error", None),
            })
        
        df = pd.DataFrame(run_data)
        return df

    def get_best_model(self) -> Dict[str, Any]:
        """
        Get the best model based on test_mean_absolute_error.
        """
        df = self.list_all_runs()
        # Filter out runs that don't have 'test_mean_absolute_error'
        df_filtered = df.dropna(subset=["test_mean_absolute_error"])
        
        # Sort by 'test_mean_absolute_error' and get the best run (lowest MAE)
        best_run = df_filtered.sort_values(by="test_mean_absolute_error").iloc[0]
        
        model_metadata = {
            "model_name": best_run["model_name"],
            "run_id": best_run["run_id"],
            "test_mean_absolute_error": best_run["test_mean_absolute_error"]
        }
        return model_metadata

    def save_best_model_metadata(self):
        """
        Save the best model metadata to a JSON file for later inference.
        """
        best_model = self.get_best_model()
        with open("src/artifacts/best_model.json", "w") as f:
            json.dump(best_model, f, indent=4)
        print(f"🏆 Best model metadata saved: {best_model['model_name']} (MAE: {best_model['test_mean_absolute_error']})")