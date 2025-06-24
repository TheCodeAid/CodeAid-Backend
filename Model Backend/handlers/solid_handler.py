from prompt_builder import PromptBuilder
from llm_client import LLMClient
from models import FileWithDependencies, RefactoringRequestData

class SolidHandler:
    def __init__(self, llmD: LLMClient, llmR: LLMClient):
        self.llmD = llmD
        self.llmR = llmR

    def detect(self, file: FileWithDependencies):
        prompt = PromptBuilder.solid_prompt(file)
        # print("prompt ", prompt)
        response =  self.llmD.send_prompt(prompt)
        # print("response ", response)
        return response[0].get("generated_text", {})
        # return {}
        # return None

    def refactor(self, file: RefactoringRequestData):
        prompt = PromptBuilder.refactor_solid_prompt(file)
        response = self.llmR.send_prompt(prompt)
        print("response ", response)
        return response
        # return  None


