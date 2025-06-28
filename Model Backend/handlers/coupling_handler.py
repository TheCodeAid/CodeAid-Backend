from prompt_builder import PromptBuilder
from llm_client import LLMClient
from models import FileWithDependencies, couplingSuggestionIn
import google.generativeai as genai
# key for coupling refactoring
API_KEY = "AIzaSyAhcxoSu-vTKLzX8AItgevQgMBxLWzzf7o"
# Configure the Gemini model
genai.configure(api_key=API_KEY)

# Choose the model (use gemini-pro for text)
model = genai.GenerativeModel("gemini-1.5-flash")

class CouplingHandler:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def detect(self, file: FileWithDependencies):
        prompt = PromptBuilder.coupling_prompt(file)
        response = self.llm.send_prompt(prompt)
        return response[0].get("generated_text", {})
        # return None 
        
    def refactor(self, file: couplingSuggestionIn):
        prompt = PromptBuilder.refactor_coupling_prompt(file)
        response = model.generate_content(prompt)

        raw_text = response.candidates[0].content.parts[0].text
        print("raw response:\n", raw_text)

        try:
            return raw_text
        except Exception as e:
            raise ValueError(f"Failed to extract JSON from model output: {e}")
