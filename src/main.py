from config.settings import settings
from data_pulling.download_data import DataDownloader
from features.feature_pipeline import FeatureEngineer
from data_pulling.read_data import load_train_test, save_processed_data
from pathlib import Path
from training.multi_model_trainer import MultiModelTrainer
from training.model_history import ModelHistory
from sklearn.linear_model import LinearRegression
from loguru import logger
from src.utils.logging_config import setup_logging


if __name__ == "__main__":
    setup_logging()
    experiment_name = "nyc-taxi-experiment"

    # Download Data
    downloader = DataDownloader(settings=settings)
    downloader.download_all()

    # Loading Data
    train_df, test_df = load_train_test(
        raw_data_directory=settings.RAW_DATA_DIRECTORY
    )

    # Feature Engineering
    numerical = ["trip_distance"]
    categorical = ["PU_DO"]
    target = "duration"

    preprocessor = FeatureEngineer()
    # Use Polars for scalability becasue each month has like 2.5 - 3 Million records!

    # Train and test df assumed to be loaded
    X_train, y_train = preprocessor.fit_transform(train_df)
    X_test, y_test = preprocessor.transform(test_df)
    
    processed_dir = Path(settings.PROCESSED_DATA_DIRECTORY)
    # Saving the processed data
    save_processed_data(
        X=X_train,
        y=y_train,
        filename="train_processed_data.npz",
        output_dir=processed_dir
    )

    save_processed_data(
        X=X_test,
        y=y_test,
        filename="test_processed_data.npz",
        output_dir=processed_dir
    )

    # Training Experiments
    # Train Model using MLflow
    models = {
        "LinearRegression": (LinearRegression, {}),
        # "XGBoost": (XGBRegressor, {"n_estimators": 100, "max_depth": 5, "learning_rate": 0.1}),
        # "LightGBM": (LGBMRegressor, {"n_estimators": 100, "num_leaves": 31})
    }

    trainer = MultiModelTrainer(experiment_name=experiment_name)
    trainer.train_all(models=models, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)

    model_history = ModelHistory(experiment_name)

    # Save best model based on `test_mean_absolute_error`
    model_history.save_best_model_metadata()

    # Optionally: print all runs for reference
    all_runs_df = model_history.list_all_runs()
    logger.info("All Runs:")
    logger.info(f"\n{all_runs_df.to_string()}")