import requests

request = requests.get("http://localhost:4567/EverythingEndpoint")

print(request.text)