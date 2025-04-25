import pandas as pd
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config.settings import AppSettings

class DataDownloader:
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.train_dir = Path(settings.RAW_DATA_DIRECTORY) / "train"
        self.test_dir = Path(settings.RAW_DATA_DIRECTORY) / "test"
        self.train_dir.mkdir(parents=True, exist_ok=True)
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def generate_month_range(self, start: str, end: str):

        start_date = datetime.strptime(start, "%Y-%m")
        end_date = datetime.strptime(end, "%Y-%m")

        # If start and end are the same, return just that month
        if start_date == end_date:
            return [start]
        
        months = []
        current = start_date
        while current <= end_date:
            months.append(current.strftime("%Y-%m"))
            current += relativedelta(months=1)
        return months

    def download_and_save_parquet_file(self, url: str, output_dir: Path):
        df = pd.read_parquet(url)
        filename = url.split("/")[-1]
        output_path = output_dir / filename
        df.to_parquet(output_path)
        print(f"✅ Saved data to {output_path}")

    def download_split(self, start: str, end: str, out_dir: Path):
        months = self.generate_month_range(start, end)
        for year_month in months:
            url = self.settings.DATA_URL.format(year_month=year_month)
            print(f"⬇️ Downloading: {url}")
            self.download_and_save_parquet_file(url, out_dir)

    def download_all(self):
        print("📥 Downloading training data...")
        self.download_split(
            self.settings.TRAINING_DATA_DATE["start"],
            self.settings.TRAINING_DATA_DATE["end"],
            self.train_dir
        )

        print("📥 Downloading testing data...")
        self.download_split(
            self.settings.TESTING_DATA_DATE["start"],
            self.settings.TESTING_DATA_DATE["end"],
            self.test_dir
        )

