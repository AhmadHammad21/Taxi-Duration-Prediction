import requests

url = 'https://iy7gped0wa.execute-api.us-east-1.amazonaws.com/dev/taxi-prediction-dev'

# Example data to send (change according to your API)
payload = {
    "feature1": 1.23,
    "feature2": 4.56
}


response = requests.post(url, json=payload)

# print the response
print(response.status_code)
print(response.json())