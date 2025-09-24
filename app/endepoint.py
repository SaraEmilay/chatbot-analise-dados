import requests

url = "http://127.0.0.1:8000/chat"
data = {"user_id": "123", "message": "Qual a média de idade por UF?"}

res = requests.post(url, json=data)
print(res.json())