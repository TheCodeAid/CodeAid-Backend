import json_repair
from huggingface_hub import InferenceClient
import requests
# from scipy.special import parameters

headers = {
	"Accept" : "application/json",
	"Authorization": "Bearer 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",
	"Content-Type": "application/json"
}

class LLMClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def parse_json(self, text):
        try:
            return json_repair.loads(text)
        except Exception:
            return None

    def send_prompt(self, prompt_text: str) -> dict:
        try:
            response = requests.post(self.api_url, headers=headers, json={
                "inputs": prompt_text,
                "parameters": {"max_new_tokens": 8192}
            })
            print(response.json())
            return response.json()
        except Exception as e:
            print("LLM Error:", e)
            return None
