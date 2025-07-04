from prompt_builder import PromptBuilder
from llm_client import LLMClient
from models import FileWithDependencies, RefactoringRequestData, RefactoringOutput,Dependency, RefactoredFile

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
        #return None

    def refactorMainFile(self, file: RefactoringRequestData):
        prompt = PromptBuilder.refactor_solid_prompt(file)
        response = self.llmR.send_prompt(prompt)
        print("response ", response)
        return response[0].get("generated_text", {})
        # return  None

    def refactorDependencyFiles(self, old_main_file: str, dependents: list[Dependency] , refactored_files: RefactoringOutput):
        prompt = PromptBuilder.refactor_dependencies(old_main_file, dependents, refactored_files)
        response = self.llmR.send_prompt(prompt)
        print("response ", response)
        return response[0].get("generated_text", {})
        # return  None
