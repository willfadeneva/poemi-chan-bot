from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://poemi-chan.onrender.com"],  # Frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENROUTER_API_KEY")

class PoemRequest(BaseModel):
    topic: str
@app.get("/")
def root():
    return {"message": "Poemi-chan poetry bot is alive!"}

@app.post("/generate_poem")
def generate_poem(req: PoemRequest):
    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {"role": "system", "content": "You are a helpful poetry bot that writes poems for Japanese kids in grades 1 to 6."},
            {"role": "user", "content": f"Write a short, simple poem about {req.topic} in English suitable for kids."}
        ],
        "max_tokens": 256,
        "temperature": 0.8,
        "top_p": 0.95,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return {"poem": data["choices"][0]["message"]["content"]}
