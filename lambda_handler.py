import json
import os
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import your existing FastAPI app
from src.app import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware for API Gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for the FastAPI application without Mangum.
    
    This function directly handles API Gateway events and routes them
    to the appropriate FastAPI endpoints.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        logger.info(f"Processing event: {event.get('httpMethod', 'UNKNOWN')} {event.get('path', 'UNKNOWN')}")
        
        # Extract request details
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters', {}) or {}
        body = event.get('body', '')
        
        # Handle different HTTP methods
        if http_method == 'GET':
            if path == '/health':
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({'status': 'healthy', 'message': 'Service is running'})
                }
            elif path == '/':
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({
                        'message': 'Taxi Duration Prediction API',
                        'version': '1.0.0',
                        'endpoints': ['/health', '/predict']
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Not Found', 'message': f'Endpoint {path} not found'})
                }
        
        elif http_method == 'POST':
            if path == '/predict':
                try:
                    # Parse the request body
                    if body:
                        request_data = json.loads(body)
                    else:
                        request_data = {}
                    
                    # Import necessary modules
                    import pandas as pd
                    from src.inference.predict import ModelPredictor
                    from src.features.feature_pipeline import FeatureEngineer
                    
                    # Create feature engineer and model predictor
                    feature_engineer = FeatureEngineer()
                    model_predictor = ModelPredictor(feature_engineer)
                    
                    # Create DataFrame from request data
                    new_data = {
                        "PULocationID": [request_data.get('PULocationID', 1)],
                        "DOLocationID": [request_data.get('DOLocationID', 1)],
                        "trip_distance": [request_data.get('trip_distance', 1.0)]
                    }
                    new_data_df = pd.DataFrame(new_data)
                    
                    # Make prediction
                    prediction = model_predictor.predict(new_data_df)
                    prediction = float(prediction[0])
                    
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                        },
                        'body': json.dumps({
                            'duration': prediction,
                            'message': 'Prediction completed successfully'
                        })
                    }
                except Exception as e:
                    logger.error(f"Prediction error: {str(e)}")
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                        },
                        'body': json.dumps({
                            'error': 'Bad Request',
                            'message': 'Invalid request data',
                            'detail': str(e) if os.getenv('APP_ENV') == 'development' else None
                        })
                    }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Not Found', 'message': f'Endpoint {path} not found'})
                }
        
        elif http_method == 'OPTIONS':
            # Handle CORS preflight requests
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': ''
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps({'error': 'Method Not Allowed', 'message': f'Method {http_method} not allowed'})
            }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'detail': str(e) if os.getenv('APP_ENV') == 'development' else None
            })
        }

# For local development (optional)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 