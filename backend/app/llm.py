from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_BASE = os.getenv("LLM_API_BASE")
MODEL = os.getenv("MODEL")

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE,
)

def get_summary_and_keywords(text: str):
    """
    Gets summary and keywords from the LLM.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text and extracts keywords.",
            },
            {
                "role": "user",
                "content": f"Please provide a 5-10 line summary and 10-20 relevant keywords (in a JSON list) for the following text:\n\n{text}",
            },
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
