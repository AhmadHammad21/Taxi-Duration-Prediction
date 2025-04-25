import json
import mlflow


## TODO DO AN INFERENCE
def load_best_model():
    # Load the best model metadata from the saved file
    with open("artifacts/best_model.json") as f:
        metadata = json.load(f)

    # Load the model from MLflow using the run ID and model name
    model_uri = f"runs:/{metadata['run_id']}/{metadata['model_name']}"
    model = mlflow.pyfunc.load_model(model_uri)
    return model

def predict(X):
    model = load_best_model()
    return model.predict(X)