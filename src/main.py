from config.settings import settings
from data_pulling.download_data import DataDownloader


if __name__ == "__main__":
    downloader = DataDownloader(settings)
    downloader.download_all()