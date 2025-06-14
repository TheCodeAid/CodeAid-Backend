import json_repair
from huggingface_hub import InferenceClient

class LLMClient:
    def __init__(self, model_id: str):
        self.client = InferenceClient(model=model_id)

    def parse_json(self, text):
        try:
            return json_repair.loads(text)
        except Exception:
            return None

    def send_prompt(self, prompt_text: str) -> dict:
        try:
            output = self.client.text_generation(prompt_text, max_new_tokens=2048)
            return self.parse_json(output)
        except Exception as e:
            print("LLM Error:", e)
            return None
