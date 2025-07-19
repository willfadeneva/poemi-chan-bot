import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/models"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
}

def list_models():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        models = response.json()
        print("Available models for your API key:")
        for m in models.get("data", []):
            print(f"- {m['id']} (Owner: {m.get('owner', 'N/A')})")
    else:
        print(f"Failed to fetch models. Status: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    list_models()
