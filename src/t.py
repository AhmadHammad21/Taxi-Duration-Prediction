import requests

url = 'https://kcqpx7zv7r4feu2j2by2ntiaqe0szpet.lambda-url.us-east-1.on.aws/api/v1/'

response = requests.get(url)
print(response)
# Example data to send (change according to your API)
# payload = {
#     "DOLocationID": "x",
#     "PULocationID": "y"
# }


# response = requests.post(url, json=payload)

# # print the response
# print(response.status_code)
# print(response.json())