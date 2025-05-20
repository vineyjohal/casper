import requests

url = "http://10.0.0.48:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.2-3b-instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the capital of Canada?"}
    ],
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())