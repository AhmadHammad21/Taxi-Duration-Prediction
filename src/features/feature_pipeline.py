import pandas as pd
import logging
from typing import List, Optional
from sklearn.feature_extraction import DictVectorizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Feature engineering pipeline for NYC taxi data with DictVectorizer.
    """

    # Constants for feature names
    PICKUP_DATETIME = "tpep_pickup_datetime"
    DROPOFF_DATETIME = "tpep_dropoff_datetime"
    AIRPORT_FEE = "Airport_fee"
    PU = "PULocationID"
    DO = "DOLocationID"
    PU_DO = "PU_DO"
    DURATION = "duration"

    def __init__(
        self,
        numerical: List[str] = None,
        categorical: List[str] = None,
        target: str = DURATION,
    ):
        self.numerical = numerical or ["trip_distance"]
        self.categorical = categorical or [self.PU_DO]
        self.target = target
        self.cols = self.numerical + self.categorical + [self.target]
        self.dv: Optional[DictVectorizer] = None

    def _clean_and_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        logger.info("Dropping rows with missing airport fee...")
        df = df[df[self.AIRPORT_FEE].notna()]

        logger.info("Converting pickup and dropoff datetime columns...")
        df[self.PICKUP_DATETIME] = pd.to_datetime(df[self.PICKUP_DATETIME])
        df[self.DROPOFF_DATETIME] = pd.to_datetime(df[self.DROPOFF_DATETIME])

        logger.info("Calculating trip duration in minutes...")
        df[self.target] = (
            df[self.DROPOFF_DATETIME] - df[self.PICKUP_DATETIME]
        ).dt.total_seconds() / 60

        logger.info("Filtering out trips with invalid durations...")
        df = df.query("duration > 0 and duration <= 90").reset_index(drop=True)

        logger.info("Creating PU_DO categorical feature...")
        df[self.PU] = df[self.PU].astype(str)
        df[self.DO] = df[self.DO].astype(str)
        df[self.PU_DO] = df[self.PU] + "_" + df[self.DO]

        logger.info("Sorting dataframe by pickup datetime...")
        df = df.sort_values(self.PICKUP_DATETIME)

        return df[self.cols]

    def fit_transform(self, df: pd.DataFrame):
        logger.info("Fitting and transforming training data...")
        df = self._clean_and_engineer(df)
        self.dv = DictVectorizer()
        features = df[self.categorical + self.numerical].to_dict(orient="records")
        X = self.dv.fit_transform(features)
        y = df[self.target].values
        logger.info("Training data transformation complete.")
        return X, y

    def transform(self, df: pd.DataFrame):
        logger.info("Transforming new data...")
        if not self.dv:
            raise ValueError("DictVectorizer not fitted. Run fit_transform first.")
        df = self._clean_and_engineer(df)
        features = df[self.categorical + self.numerical].to_dict(orient="records")
        X = self.dv.transform(features)
        y = df[self.target].values
        logger.info("Data transformation complete.")
        return X, y
