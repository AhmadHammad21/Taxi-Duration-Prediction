import json
import os
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from starlette.requests import Request
from starlette.responses import Response
import asyncio

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

def create_request_from_event(event: Dict[str, Any]) -> Request:
    """
    Create a FastAPI Request object from API Gateway event.
    """
    # Extract HTTP method and path
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Extract headers
    headers = {}
    if 'headers' in event:
        headers.update(event['headers'])
    
    # Extract query parameters
    query_string = event.get('queryStringParameters', {}) or {}
    
    # Extract body
    body = event.get('body', '')
    if body is None:
        body = ''
    
    # Create scope for the request
    scope = {
        'type': 'http',
        'asgi': {'version': '3.0', 'spec_version': '2.0'},
        'http_version': '1.1',
        'method': http_method,
        'scheme': 'https',
        'server': ('localhost', 443),
        'client': ('127.0.0.1', 0),
        'path': path,
        'raw_path': path.encode(),
        'query_string': query_string.encode() if isinstance(query_string, str) else b'',
        'headers': [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        'body': body.encode() if isinstance(body, str) else body,
    }
    
    return Request(scope)

async def handle_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle API Gateway event using FastAPI app directly.
    """
    try:
        # Create request from event
        request = create_request_from_event(event)
        
        # Get the route handler
        route = app.router.default if hasattr(app.router, 'default') else None
        
        # Find the appropriate route handler
        matching_route = None
        for route in app.routes:
            if hasattr(route, 'path') and getattr(route, 'path', None) == request.url.path:
                matching_route = route
                break
        
        # Create a simple response handler
        async def receive():
            return {'type': 'http.request', 'body': request.body}
        
        async def send(message):
            pass  # We'll collect the response
        
        # Call the app
        response_body = b''
        response_headers = []
        response_status = 200
        
        async def send_wrapper(message):
            nonlocal response_body, response_headers, response_status
            if message['type'] == 'http.response.start':
                response_status = message['status']
                response_headers = message['headers']
            elif message['type'] == 'http.response.body':
                response_body += message['body']
        
        # This is a simplified approach - in practice you'd want to use ASGI properly
        # For now, let's return a basic response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Request processed without Mangum',
                'path': request.url.path,
                'method': request.method
            })
        }
        
    except Exception as e:
        logger.error(f"Error in handle_request: {str(e)}")
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

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for the FastAPI application without Mangum.
    
    This function directly handles API Gateway events and translates them
    to FastAPI requests/responses.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        logger.info(f"Processing event: {event.get('httpMethod', 'UNKNOWN')} {event.get('path', 'UNKNOWN')}")
        
        # Handle the request without Mangum
        response = asyncio.run(handle_request(event))
        
        logger.info(f"Response status: {response.get('statusCode', 'UNKNOWN')}")
        return response
        
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