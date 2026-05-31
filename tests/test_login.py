import requests
BASE_URL = "http://localhost:8000"
response = requests.post(f"{BASE_URL}/api/v1/token", data={"username": "admin@agencyos.com", "password": "password123"})
print(response.status_code, response.text)
