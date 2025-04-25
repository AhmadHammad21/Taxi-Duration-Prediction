# Taxi Fare Prediction

Short description of the project.

## Project Overview
Brief explanation of what problem this project solves and why it's important.

## Data
Description of the data used, including sources and key characteristics.
Data from [TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Model
Overview of the modeling approach and key algorithms used.

## Results
Summary of model performance and key findings.

## Setup and Installation

### Installation

### Clone the Repository
```bash
git clone https://github.com/AhmadHammad21/Taxi-Duration-Prediction.git
cd Taxi-Duration-Prediction
```

### Install UV Package Manager
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv init

# Syncing the dependencies to your environment
uv sync
```

## Usage

### Run the MLFlow Server
To track machine learning experiments.
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

### Run Data, Feature, Training Pipeline
```bash
python src/main.py
```

### API Service
```bash
cd deployment
docker-compose up -d
```

### Run the FastAPI Server
```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure
Brief explanation of the repository organization.
```
taxi-duration-prediction/
├── src/                     # Source code for all the ML pipelines and services
│ ├── artifacts/             # Models Artifacts
│ ├── config/                # Configurations
│ ├── data_pulling/          # Data download & collection code
│ ├── features/               # Feature engineering pipeline code
│ ├── inference/             # Inference pipeline code
│ ├── training/              # Training service code
│ └── routes/                # API's routes
│ └── schemas/               # Schemas for validation
│ └── utils/                 # Utilities functions and helpers
├── .env.example             # Example environment variables template
├── pyproject.toml           # Project dependencies
```

## To-do List:
- ✅ Structure the project and modules
- ✅ Script to download data
- ✅ Preprocessing & feature engineering
- ✅ MLflow, Artifacts, Model Registry, Training Pipeline
- [ ] Inference Pipeline
- [ ] FastAPI API
- [ ] Add Workflow (CI/CD)
- [ ] Docker / Docker Compose
- [ ] Monitoring
- [ ] Add Tests
- [ ] Grafana / Prometheus
- [ ] Add Kubernetes
- [ ] Add diagram of project flow
- [ ] Move the data to the cloud


## Time taken to build this project
- 6 Hours

## Contributing
Anyone can contribute

## License
I don't own the data for the NYC, I'm using it for educational purposes.  
This project is licensed under the MIT License - see the LICENSE file for details.
