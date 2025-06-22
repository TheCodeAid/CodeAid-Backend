from prompt_builder import PromptBuilder
from llm_client import LLMClient
from models import FileWithDependencies, RefactoringRequestData

class SolidHandler:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def detect(self, file: FileWithDependencies):
        prompt = PromptBuilder.solid_prompt(file)
        # print("prompt ", prompt)
        # return self.llm.send_prompt(prompt)
        return None

    def refactor(self, file: RefactoringRequestData):
        prompt = PromptBuilder.refactor_solid_prompt(file)
        # return self.llm.send_prompt(prompt)
        return  None


