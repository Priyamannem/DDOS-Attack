import requests
import json

try:
    response = requests.get("http://localhost:8000/admin/traffic/stats?minutes=60")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
