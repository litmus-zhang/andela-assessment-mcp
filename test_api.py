import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_raw_call():
    base_url = os.getenv("AGENTIC_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "hello"}]
    }
    
    print(f"Calling URL: {url}")
    response = httpx.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

if __name__ == "__main__":
    test_raw_call()
