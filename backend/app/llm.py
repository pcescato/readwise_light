import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_URL")  # ex: https://openrouter.ai/api/v1
MODEL = os.getenv("MODEL")  # ex: qwen/qwen3-30b-a3b:free


def get_summary_and_keywords(text: str):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text and extracts keywords.",
            },
            {
                "role": "user",
                "content": f"Please provide a JSON object with two fields: 'summary' (a 5-10 line text summary) and 'keywords' (a list of 10-20 relevant keywords) for the following text. Output must be valid JSON only.\n\n{text}",
            },
        ],
        "temperature": 0.7,
    }

    response = requests.post(
        f"{API_BASE}/chat/completions", headers=headers, data=json.dumps(payload)
    )

    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

