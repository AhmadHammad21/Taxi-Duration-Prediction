# ml-project/
# │
# ├── .github/                    # GitHub specific files
# │   ├── workflows/              # GitHub Actions workflows
# │   │   └── ci.yml              # Continuous Integration workflow
# │   └── ISSUE_TEMPLATE/         # Issue templates
# │
# ├── .gitignore                  # Files to ignore in git
# ├── LICENSE                     # Project license
# ├── README.md                   # Project overview and instructions
# ├── requirements.txt            # Python dependencies
# ├── setup.py                    # Package installation script
# │
# ├── config/                     # Configuration files
# │   ├── config.yaml             # Main configuration
# │   ├── model_config.yaml       # Model hyperparameters
# │   └── feature_config.yaml     # Feature engineering settings
# │
# ├── data/                       # Data directory (often gitignored)
# │   ├── raw/                    # Raw, immutable data
# │   ├── processed/              # Cleaned and processed data
# │
# ├── docs/                       # Documentation
# │   ├── data_dictionary.md      # Data field descriptions
# │   ├── model_architecture.md   # Model design documentation
# │   └── experiment_tracking.md  # Experiment results and notes
# │
# ├── logs/                       # Log files
# │   └── training_logs/          # Model training logs
# │
# ├── models/                     # Saved model files
# │   ├── trained/                # Trained model artifacts
# │   └── pretrained/             # Pre-trained models
# │
# ├── notebooks/                  # Jupyter notebooks
# │   ├── 01-data-exploration.ipynb     # Initial data exploration
# │   ├── 02-feature-engineering.ipynb  # Feature development
# │   ├── 03-model-training.ipynb       # Model training experiments
# │   └── 04-model-evaluation.ipynb     # Model evaluation
# │
# ├── scripts/                    # Utility scripts
# │   ├── data_download.py        # Script to download data
# │   ├── preprocess.py           # Data preprocessing script
# │   ├── train_model.py          # Model training script
# │   └── evaluate_model.py       # Model evaluation script
# │
# ├── src/                        # Source code
# │   ├── __init__.py             # Make src a Python package
# │   │
# │   ├── data/                   # Data processing code
# │   │   ├── __init__.py
# │   │   ├── make_dataset.py     # Data acquisition and generation
# │   │   ├── preprocess.py       # Data cleaning and transformation
# │   │   └── validation.py       # Data validation utilities
# │   │
# │   ├── features/               # Feature engineering code
# │   │   ├── __init__.py
# │   │   ├── build_features.py   # Feature creation
# │   │   └── transformers.py     # Custom feature transformers
# │   │
# │   ├── models/                 # Model code
# │   │   ├── __init__.py
# │   │   ├── train_model.py      # Model training functionality
# │   │   ├── predict_model.py    # Model prediction functionality
# │   │   ├── evaluate_model.py   # Model evaluation metrics
# │   │   └── model_registry.py   # Model versioning & registry
# │   │
# │   └── utils/                  # Utility functions
# │       ├── __init__.py
# │       ├── logger.py           # Logging configuration
# │       ├── config_parser.py    # Configuration parser
# │       └── io_utils.py         # I/O utilities
# │
# ├── tests/                      # Test suite
# │   ├── __init__.py
# │   ├── conftest.py             # Test configuration
# │   ├── test_data.py            # Data tests
# │   ├── test_features.py        # Feature tests
# │   └── test_models.py          # Model tests
# │
# ├── mlflow/                     # MLflow experiment tracking
# │   └── mlruns/                 # MLflow run data
# │
# └── deployment/                 # Deployment configuration
#     ├── Dockerfile              # Docker container definition
#     ├── docker-compose.yml      # Docker service configuration
#     ├── kubernetes/             # Kubernetes manifests
#     │   ├── deployment.yaml     # K8s deployment
#     │   └── service.yaml        # K8s service
#     ├── api/                    # API code
#     │   ├── app.py              # FastAPI application
#     │   └── routes/             # API endpoints
#     └── monitoring/             # Monitoring configuration
#         ├── prometheus.yml      # Prometheus configuration
#         └── grafana/            # Grafana dashboards
