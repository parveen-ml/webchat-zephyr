import os
import requests
from dotenv import load_dotenv

# Load the .env file
print("Loading .env file...")
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

if HF_API_KEY is None:
    print("API key not loaded! Check .env file and variable name.")
    exit()
else:
    print("API Key Loaded:", HF_API_KEY[:10], "...")

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()

        # Handle Hugging Face response
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].split(prompt)[-1].strip()
        else:
            return "⚠️ Unexpected model response format."

    except Exception as e:
        return f"Error: {e}"
