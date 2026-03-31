import requests
import json

url = "http://localhost:5000/api/knowledge/webhook/status"
payload = {"source_id": "507f1f77bcf86cd799439011", "status": "processing"}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.status_code, response.text)
except Exception as e:
    print("Error:", e)
