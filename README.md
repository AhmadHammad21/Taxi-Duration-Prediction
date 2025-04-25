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
# windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv init

# Syncing the dependencies to your environment
uv sync
```

## Usage

### Data Preparation
```bash
python src/data_download.py
python src/preprocess.py
```

### Model Training
```bash
python src/train_model.py
```

### Model Evaluation
```bash
python src/evaluate_model.py
```

### API Service
```bash
cd deployment
docker-compose up -d
```

## Project Structure
Brief explanation of the repository organization.
```
llm-twin-course/
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
- [ ] Preprocessing / feature engineering
- [ ] MLflow / CometML
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
