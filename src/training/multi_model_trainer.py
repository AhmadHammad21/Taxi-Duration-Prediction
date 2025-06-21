from typing import Dict, Any, Tuple
from sklearn.base import RegressorMixin
from .trainer import ModelTrainer
from loguru import logger


class MultiModelTrainer:
    def __init__(self, experiment_name: str = "nyc-taxi-experiment"):
        self.model_trainer = ModelTrainer(experiment_name=experiment_name)

    def train_all(
        self,
        models: Dict[str, Tuple[RegressorMixin, Dict[str, Any]]],
        X_train,
        y_train,
        X_test,
        y_test
    ):
        for model_name, (model_cls, params) in models.items():
            logger.info(f"🚀 Training {model_name}...")
            model = model_cls(**params)
            self.model_trainer.train(
                model=model,
                model_name=model_name,
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test
            )
            logger.info(f"🚀 Finished Training {model_name}...")
