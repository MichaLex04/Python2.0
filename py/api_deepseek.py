# py/api_deepseek.py
import requests
import os

DEESEEK_API_URL = "https://api.deepseek.ai/v1/generate_recipe"
DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")

def generar_receta_ia(prompt):
    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 500
    }
    response = requests.post(DEESEEK_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("recipe_text", "")
    else:
        raise Exception(f"Error API DeepSeek: {response.status_code} {response.text}")