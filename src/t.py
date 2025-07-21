import requests

url = 'https://kcqpx7zv7r4feu2j2by2ntiaqe0szpet.lambda-url.us-east-1.on.aws/api/v1/predict'

# response = requests.get(url)
# print(response)
# Example data to send (change according to your API)
payload = {
    "DOLocationID": "1",
    "PULocationID": "2",
    "trip_distance": 5
}


response = requests.post(url, json=payload)

# print the response
print(response.status_code)
print(response.json())