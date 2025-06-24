import json
from models import FileWithDependencies, RefactoringOutput, RefactoringRequestData, SolidDetectionOutput, CouplingDetectionOutput


class PromptBuilder:
    
    from models import RefactoringRequestData

class PromptBuilder:

    @staticmethod
    def build_code_bundle_refactor(file: RefactoringRequestData) -> dict:
        return {
            "prompt": {
                "mainFilePath": file.mainFilePath,
                "mainFileContent": file.content,
                "dependencies": [
                    {
                        "filePath": dep.depFilePath,
                        "fileContent": dep.content
                    } for dep in file.dependencies
                ]
            },
            "violations": [
                {
                    "principle": v.principle,
                    "justification": v.justification
                } for v in file.violations
            ]
        }

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


    @staticmethod
    def refactor_solid_prompt(file: FileWithDependencies) -> str:
        code = PromptBuilder.build_code_bundle_refactor(file)
        return "\n".join([
            "You are an expert Java developer specialized in applying Single Responsibility and Open-Closed principles through code refactoring.",
            "You will be given one main Java file, with some dependencies (maybe none) along with a structured JSON detailing the detected Single Responsibility, Open-Closed violations in the main file.",
            "Your task is to refactor the code to eliminate these violations while maintaining and improving overall code clarity and design.",
            "",
            "For reference, here are brief descriptions of the SRP and OCP principles:",
            "- SRP (Single Responsibility): A class should have only one reason to change, i.e., one responsibility.",
            "- OCP (Open/Closed): Classes should be open for extension, but closed for modification.",
            "Apply a step-by-step reasoning process to identify the best approach for refactoring each violation.",
            "After making initial changes, re-evaluate the result and improve it further if needed.",
            "Then, reflect on the outcome: did you miss anything? Did your refactoring introduce new issues? If so, revise accordingly.",
            "You should return the main file in case of being updated with its updated content.",
            "You should return the created files with its content.",
            "Never add multiple classes/enums/interfaces in the same file; if needed, create a new file for each.",
            "After refactoring the main file and adding any new files, you must:",
            "- Review all dependency files for references to the main file’s class, methods, or fields.",
            "- Update those dependency files to reflect any renames, deletions, or new methods introduced in your refactor.",
            "- Ensure there are no invalid references in dependency files (such as calling a method that no longer exists).",
            "All updated dependency files should be included in your output alongside the main file and new files, following the Pydantic schema format.",
            "Don't return a file unless it is updated or created.",
            "",
            "## Critical Output and Formatting Rules:",
            "1. **Comment Formatting for Unfixable Dependencies:** This is a strict requirement. If a dependency cannot be updated due to missing context, you must leave a comment. IT IS CRITICAL that you add a line break (`\\n`) immediately after the comment. The code that follows the comment MUST start on a new line to avoid compilation errors.",
            "2. **No Extra Content:** Do not include any explanation, introduction, or conclusion outside the final JSON output.",
            "3. **Code Formatting:** Return the code in one line without extra spaces or break lines. Don't add any comments.",
            "4. **JSON Structure:** You must follow the format defined in the Pydantic schema for the refactoring output.",
            "",
            "Be precise, complete, and objective. If no changes are needed, reflect that in the response.",
            "## Code:",
            json.dumps(code["prompt"], ensure_ascii=False),
            "",
            "## SO Violations:",
            json.dumps(code["violations"], ensure_ascii=False),
            "",
            "## Pydantic Details:",
            json.dumps(RefactoringOutput.model_json_schema(), ensure_ascii=False),
            "",
            "## Refactored Code:",
            "```json"
        ])

    @staticmethod
    def coupling_prompt(file: FileWithDependencies) -> str:
        code = PromptBuilder.build_code_bundle(file)
        return "\n".join([
            "You are a software engineer.",
            "You will be given one file with its file dependencies.",
            "Your task is to identify and explain any of the following coupling smells:",
            "",
            "- Feature Envy: A method that seems more interested in another class than the one it is in, accessing its data and methods frequently.",
            "- Inappropriate Intimacy: Two classes that share too much information or access each other's internal details excessively.",
            "- Incomplete Library Class: A library class is missing functionality that should be there, forcing users to add methods or subclasses that break encapsulation.",
            "- Message Chains: A client asks one object for another object, then that object for another, and so on, forming a long chain of calls.",
            "- Middle Man: A class that delegates almost everything to another class and does very little itself.",
            "",
            "Use a step-by-step reasoning process (Chain of Thought) to evaluate if any of these smells exist in the code.",
            "For each suspected smell, explain what triggered it, and which class/method is involved.",
            "",
            "After your first pass, review your analysis and refine it if necessary.",
            "Then, critically evaluate your final result.",
            "- Did you miss any smell?",
            "- Did you misclassify anything?",
            "- Could your reasoning be more precise?",
            "",
            "Always respond in a structured JSON format. Do not include any explanation outside the JSON.",
            "You have to extract Coupling code smells from Code according the Pydantic details.",
            "Be objective and thorough, even if no violations are found.",
            "Do not generate any introduction or conclusion.",
            "## Code:",
            json.dumps(code, ensure_ascii=False),
            "",
            "## Pydantic Details:",
            json.dumps(CouplingDetectionOutput.model_json_schema(), ensure_ascii=False),
            "",
            "## Coupling code smells:",
            "json"
        ])

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
