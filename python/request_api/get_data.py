import requests, json

# request = requests.get("http://localhost:4567/EverythingEndpoint")
# request = requests.get("http://localhost:8080/api/v1/news/summary")
payload = {
    "model": "llama3.1:8b",
    # "messages": [{"role": "user", "content": "hello"}]
    "prompt": "Give me a brief but interesting fact.", 
    "stream": True
}
request = requests.post("http://localhost:11434/api/generate", json=payload)
response = request.text
split_response = response.split("\"response\":\"")
# "\",\"done\""
new_string = []
for index, x in enumerate(split_response):
    if index % 2 == 1:
        new_string.append(x.split("\",\"done\""))
        print(x.split("\",\"done\""))
        print()

