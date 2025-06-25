from prompt_builder import PromptBuilder
from llm_client import LLMClient
from models import FileWithDependencies

class CouplingHandler:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def detect(self, file: FileWithDependencies):
        prompt = PromptBuilder.coupling_prompt(file)
        response = self.llm.send_prompt(prompt) #####################
        return response[0].get("generated_text", {})
        # return None 
        
    def refactor(self, file: FileWithDependencies):
        prompt = PromptBuilder.refactor_coupling_prompt(file)
        return self.llm.send_prompt(prompt)
