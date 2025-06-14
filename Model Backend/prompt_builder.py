import json
from models import FileWithDependencies, SolidDetectionOutput

class PromptBuilder:
    @staticmethod
    def build_code_bundle(file: FileWithDependencies):
        return {
            "main": {
                "filePath": file.mainFilePath,
                "content": file.content
            },
            "dependencies": [
                {"filePath": d.depFilePath, "content": d.content} for d in file.dependencies
            ]
        }

    @staticmethod
    def solid_prompt(file: FileWithDependencies) -> str:
        code = PromptBuilder.build_code_bundle(file)
        return "\n".join([
            "You are a senior software engineer.",
            "You will be given one file with its file dependencies.",
            "Your task is to detect violations of SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.",
            "",
            "Principle definitions (apply these strictly):",
            "SRP: A class has exactly one reason to change—only one responsibility.",
            "OCP: A class may be extended without modifying its existing code.",
            "LSP: Subtypes must behave interchangeably with their base types.",
            "ISP: Clients should only depend on the methods they actually use.",
            "DIP: High‑level (policy/business) modules must depend on abstractions (interfaces/abstract classes), not on concrete (implementation) classes. Low‑level modules must implement those abstractions; they should NOT be directly referenced by high‑level modules.",
            "Don't include the usage of built in classes (e.g. java.util.Scanner, java.lang.String, List, Map), they don't break DIP",
            "",
            "Apply a step-by-step reasoning process to identify any violations.",
            "Start by explaining what each principle means in the current context, and how the code complies or fails to comply with it.",
            "",
            "After providing your first assessment, re-evaluate your findings and refine your judgment if necessary.",
            "",
            "Finally, reflect on your answer: did you miss anything? Could your answer be improved? If so, revise accordingly.",
            "",
            "Always respond in a structured JSON format. Do not include any explanation outside the JSON.",
            "You have to extract SOLID Violations from Code according the Pydantic details.",
            "Be objective and thorough, even if no violations are found.",
            "Do not generate any introduction or conclusion."
            "## Code:",
            json.dumps(code, ensure_ascii=False),
            "",

            "## Pydantic Details:",
            json.dumps(
                SolidDetectionOutput.model_json_schema(), ensure_ascii=False
            ),
            "",
            "## SOLID Violations:",
            "json"
        ])


    # @staticmethod
    # def refactor_solid_prompt(file: FileWithDependencies) -> str:
    #     code = PromptBuilder.build_code_bundle(file)
    #     return "\n".join([
    #         "You are a senior software engineer.",
    #         "Refactor the code to fix SOLID violations. Return only the refactored version of the main file.",
    #         "## Code:",
    #         json.dumps(code, ensure_ascii=False),
    #         "",
    #         "## Response format:",
    #         '{"refactoredCode": "..."}'
    #     ])

    # @staticmethod
    # def coupling_prompt(file: FileWithDependencies) -> str:
    #     code = PromptBuilder.build_code_bundle(file)
    #     return "\n".join([
    #         "You are a senior software engineer.",
    #         "Detect coupling smells (like Feature Envy, Inappropriate Intimacy, etc.).",
    #         "Respond in structured JSON only.",
    #         "## Code:",
    #         json.dumps(code, ensure_ascii=False),
    #         "",
    #         "## Response format:",
    #         '{"couplingSmells": [{"filesPaths": [...], "smells": [{"smell": "...", "justification": "..."}]}]}'
    #     ])

    # @staticmethod
    # def refactor_coupling_prompt(file: FileWithDependencies) -> str:
    #     code = PromptBuilder.build_code_bundle(file)
    #     return "\n".join([
    #         "You are a senior software engineer.",
    #         "Refactor the code to reduce coupling smells. Return only the refactored version of the main file.",
    #         "## Code:",
    #         json.dumps(code, ensure_ascii=False),
    #         "",
    #         "## Response format:",
    #         '{"refactoredCode": "..."}'
    #     ])
