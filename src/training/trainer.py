import mlflow
import mlflow.sklearn
import mlflow.lightgbm
import mlflow.xgboost
import json
from pathlib import Path
from .mlflow_utils import log_regression_metrics_run


class ModelTrainer:
    def __init__(self, experiment_name: str = "nyc-taxi-experiment",
                 tracking_uri: str = "sqlite:///mlflow.db"):
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri

        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

        mlflow.autolog(log_datasets=False)
        mlflow.xgboost.autolog(log_datasets=False)
        mlflow.lightgbm.autolog(log_datasets=False)

    def train(self, model, model_name: str, X_train, y_train, X_test, y_test):
        with mlflow.start_run():
            model.fit(X_train, y_train)

            y_pred_test = model.predict(X_test)
            y_pred_train = model.predict(X_train)

            log_regression_metrics_run(
                y_true=y_train, predictions=y_pred_train,
                prefix="train", n_features=X_train.shape[1]
            )
            log_regression_metrics_run(
                y_true=y_test, predictions=y_pred_test,
                prefix="test", n_features=X_train.shape[1]
            )

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path=model_name,
                registered_model_name=model_name
            )

    def _save_best_model_info(self):
        best_model = min(self.run_scores.items(), key=lambda item: item[1]["mae"])
        model_name, info = best_model

        metadata = {
            "model_name": model_name,
            "run_id": info["run_id"],
            "mae": info["mae"]
        }

        Path("artifacts").mkdir(exist_ok=True)
        with open("artifacts/best_model.json", "w") as f:
            json.dump(metadata, f, indent=4)

        print(f"🏆 Best model: {model_name} with MAE: {info['mae']}")
        print("📁 Saved best model metadata to artifacts/best_model.json")