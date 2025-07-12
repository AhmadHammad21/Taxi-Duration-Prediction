#!/usr/bin/env python3
"""
Script to extract model directly from MLflow artifacts and save as pickle.
This bypasses MLflow tracking entirely.
"""

import os
import json
import pickle
import shutil
from pathlib import Path

def extract_model_from_mlflow():
    """Extract model directly from MLflow artifacts"""
    
    # Load the best model metadata
    with open("src/artifacts/best_model.json") as f:
        metadata = json.load(f)
    
    run_id = metadata["run_id"]
    print(f"Extracting model from run: {run_id}")
    
    # Find the model path in mlruns
    model_path = None
    for experiment_id in os.listdir("mlruns"):
        exp_path = os.path.join("mlruns", experiment_id)
        if not os.path.isdir(exp_path):
            continue
        run_dir = os.path.join(exp_path, run_id)
        if os.path.exists(run_dir):
            # Look for the model in artifacts
            artifacts_dir = os.path.join(run_dir, "artifacts")
            if os.path.exists(artifacts_dir):
                # Check for model directory
                model_dir = os.path.join(artifacts_dir, "model")
                if os.path.exists(model_dir):
                    model_path = model_dir
                    break
                # Check for LinearRegression directory
                lr_dir = os.path.join(artifacts_dir, "LinearRegression")
                if os.path.exists(lr_dir):
                    model_path = lr_dir
                    break
    
    if not model_path:
        print(f"Model not found for run {run_id}")
        return False
    
    print(f"Found model at: {model_path}")
    
    # Load the model using pickle (direct approach)
    try:
        # Look for model.pkl in the model directory
        model_pkl_path = os.path.join(model_path, "model.pkl")
        if os.path.exists(model_pkl_path):
            print(f"Loading model from: {model_pkl_path}")
            with open(model_pkl_path, 'rb') as f:
                model = pickle.load(f)
            print(f"Successfully loaded model from: {model_pkl_path}")
        else:
            print(f"model.pkl not found in {model_path}")
            print("Available files:")
            for file in os.listdir(model_path):
                print(f"  - {file}")
            return False
        
        # Save as simple pickle
        output_path = "src/artifacts/simple_model.pkl"
        with open(output_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model saved as pickle to: {output_path}")
        print(f"Model type: {type(model)}")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

if __name__ == "__main__":
    success = extract_model_from_mlflow()
    if success:
        print("✅ Model extraction successful!")
    else:
        print("❌ Model extraction failed!") 