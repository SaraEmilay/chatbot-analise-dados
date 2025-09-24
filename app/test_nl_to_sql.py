import requests

url = "http://127.0.0.1:8000/nl-to-sql"
payload = {
    "question": "Liste o consumo médio dos clientes no bairro SAN MARTIN em 2022"
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
