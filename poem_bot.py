import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost",  # Required
    "X-Title": "Poemi-chan Poetry Bot",  # Optional
    "Content-Type": "application/json"
}


def get_poem(prompt, model="anthropic/claude-3-haiku"):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are Poemi-chan, a cheerful AI that writes simple and fun English poems for Japanese children aged 6 to 12 learning English. Keep it short, friendly, and easy to understand."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Print any error details if response fails
    if response.status_code != 200:
        print("ERROR:", response.status_code)
        print("DETAILS:", response.text)
        response.raise_for_status()

    return response.json()['choices'][0]['message']['content']


if __name__ == "__main__":
    topic = input("What should the poem be about? ")
    prompt = f"Write a short and simple English poem about {topic}, suitable for a Japanese child in grade 1 to 6 who is learning English."
    poem = get_poem(prompt)
    print("\n🎵 Poem Generated:\n")
    print(poem)
