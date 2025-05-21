# test/test_main_api.py

import requests
from requests.exceptions import ConnectionError

API_URL = "http://127.0.0.1:8000/query"

def test_query():
    payload = {"question": "What is the criteria to get admission in BS computer science program"}
    
    try:
        response = requests.post(API_URL, json=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except ConnectionError:
        print("❌ Error: Could not connect to the FastAPI server. Is it running at http://127.0.0.1:8000?")

if __name__ == "__main__":
    test_query()
