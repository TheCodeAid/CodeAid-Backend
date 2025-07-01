import json
from typing import Dict, List
from models import FileWithDependencies, RefactoredFile, RefactoringOutput, RefactoringRequestData, SolidDetectionOutput, CouplingDetectionOutput,Dependency, couplingSuggestionIn, couplingSuggestionOut


class PromptBuilder:
    
    from models import RefactoringRequestData

class PromptBuilder:

    @staticmethod
    def build_code_bundle_refactor(file: RefactoringRequestData) -> dict:
        return {
            "prompt": {
                "mainFilePath": file.data[0].mainFilePath,
                "mainFileContent": file.data[0].mainFileContent,
            },
            "violations": [
                {
                    "principle": v.principle,
                    "justification": v.justification
                } for v in file.violations
            ]
        }
    
    @staticmethod
    def build_code_bundle_refactor_dep(old_main_file: str, dependents: list[Dependency], refactored_files: list[RefactoredFile]) -> dict:
        return {
            "old": {
                "mainFileContent": old_main_file,
            },
            "new": {
                "refactored_files": refactored_files, 
            },
            "dependents": [
                {
                    "filePath": dep.depFilePath,
                    "fileContent": dep.depFileContent
                } for dep in dependents
            ]  
        }
    
    @staticmethod
    def build_coupling_code_bundle_refactor(input_data: couplingSuggestionIn) -> dict:
        return {
            "coupling_smells": [
                {
                    "files": [
                        {
                            "filePath": f.filePath,
                            "fileContent": f.content
                        } for f in violation.files
                    ],
                    "smells": [
                        {
                            "smell": s.smell,
                            "justification": s.justification
                        } for s in violation.smells
                    ]
                }
                for violation in input_data.coupling_smells
            ]
        }
    
    @staticmethod
    def build_code_bundle(file: FileWithDependencies):
        return {
            "main": {
                "filePath": file.mainFilePath,
                "content": file.mainFileContent
            },
            "dependencies": [
                {"filePath": d.depFilePath, "content": d.depFileContent} for d in file.dependencies
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
    def refactor_solid_prompt(file: RefactoringRequestData) -> str:
        code = PromptBuilder.build_code_bundle_refactor(file)
        return "\n".join([
            "You are an expert Java developer specialized in applying Single Responsibility and Open-Closed principles through code refactoring.",
            "You will be given one main Java file, along with a structured JSON detailing the detected Single Responsibility, Open-Closed violations in the main file.",
            "Your task is to refactor the code to eliminate these violations while maintaining and improving overall code clarity and design.",

            "For reference, here are brief descriptions of the SRP and OCP principles:",
            "- SRP (Single Responsibility): A class should have only one reason to change, i.e., one responsibility.",
            "- OCP (Open/Closed): Classes should be open for extension, but closed for modification.",
            "Apply a step-by-step reasoning process to identify the best approach for refactoring each violation.",
            "After making initial changes, re-evaluate the result and improve it further if needed.",
            "Then, reflect on the outcome: did you miss anything? Did your refactoring introduce new issues? If so, revise accordingly.",
            "You should return the main file in case of being updated with its updated content.",
            "You should return the created files with their content.",
            "Never add multiple classes/enums/interfaces in the same file; if needed, create a new file for each.",
            "Don't return a file unless it is updated or created.",
            "Don't return a code with syntax errors.",

            "## Critical Output and Formatting Rules:",
            "1. **Comment Formatting for Unfixable Dependencies:** This is a strict requirement. If a dependency cannot be updated due to missing context, you must leave a comment. IT IS CRITICAL that you add a real line break after the comment. The code that follows the comment MUST start on a new line to avoid compilation errors.",
            "2. **No Extra Content:** Do not include any explanation, introduction, or conclusion outside the final JSON output.",
            "3. **Code Formatting:** Return the code with proper indentation and real newlines. DO NOT encode line breaks as '\\n'. The code must be syntactically valid and parsable by a Java parser.",
            "4. **No Escaped Strings:** Do NOT escape newlines, quotes, or slashes. Return clean, raw Java code within the JSON.",
            "5. **JSON Structure:** You must follow the format defined in the Pydantic schema for the refactoring output.",

            "Be precise, complete, and objective. If no changes are needed, reflect that in the response.",

            "## Code:",
            json.dumps(code["prompt"], ensure_ascii=False),

            "## SO Violations:",
            json.dumps(code["violations"], ensure_ascii=False),

            "## Pydantic Details:",
            json.dumps(RefactoringOutput.model_json_schema(), ensure_ascii=False),

            "## Refactored Code:",
            "```json"
        ])

    @staticmethod
    def refactor_dependencies( old_main_file: str, dependents: list[Dependency] , refactored_files:  list[RefactoredFile]) -> str:
        code = PromptBuilder.build_code_bundle_refactor_dep(old_main_file, dependents, refactored_files)
        return "\n".join([
            "You are an expert Java developer specialized in updating all provided dependent files to be compatible with a newly refactored version of a Java class.",

            "Context:",
            "You are given:",
            "- The original version of the main Java class (Main File - OLD)",
            "- The refactored version of the main class (Main File - NEW)",
            "- Any new classes created during refactoring",
            "- A list of dependent files that previously referenced the old main file",

            "These dependents must now be updated to reference and interact correctly with the new main file and its updated structure.",
            "Follow this step-by-step process:",

            "1. Understand the changes:",
            "- Compare the old and new versions of the main file.",
            "- Identify renamed, moved, or removed methods, fields, and classes.",
            "- Understand how the newly created classes relate to the refactoring.",

            "2. Update dependents:",
            "- For each dependent file:",
            "    - Locate references to the old structure.",
            "    - Modify imports, method calls, field accesses, or object instantiations to match the new design.",
            "    - Ensure compatibility with newly introduced classes or interfaces.",

            "3. Iterative improvement:",
            "- After updating each file, assess whether it fully conforms to the refactored structure.",
            "- Make any additional modifications if inconsistencies or outdated patterns remain.",

            "4. Self-Critique & Validation:",
            "- After all updates, analyze your changes:",
            "    - Did you miss any reference to the old class structure?",
            "    - Are there inconsistencies or deprecated usages?",
            "    - Are there redundant imports or logic?",
            "- Fix issues accordingly and explain key changes and justifications.",

            "## Critical Output and Formatting Rules:",
            "1. **Comment Formatting for Unfixable Dependencies:** This is a strict requirement. If a dependency cannot be updated due to missing context, you must leave a comment. IT IS CRITICAL that you add a line break (`\\n`) immediately after the comment. The code that follows the comment MUST start on a new line to avoid compilation errors.",
            "2. **No Extra Content:** Do not include any explanation, introduction, or conclusion outside the final JSON output.",
            "3. **Code Formatting:** Return the code in one line without extra spaces or break lines. Don't add any comments.",
            "4. **JSON Structure:** You must follow the format defined in the Pydantic schema for the refactoring output.",
            "Don't return a code with syntax errors.",
            "Be precise, complete, and objective. If no changes are needed, reflect that in the response.",
            "## Old Main File:",
            json.dumps(code["old"], ensure_ascii=False),
            "",
            "## New Main file with new classes created during refactoring:",
            json.dumps(code["new"], ensure_ascii=False),
            "",
            "## Dependents:",
            json.dumps(code["dependents"], ensure_ascii=False),
            "",
            "## Pydantic Details:",
            json.dumps(RefactoringOutput.model_json_schema(), ensure_ascii=False),
            "",
            "## Refactored Dependencies:",
            "```json"
        ])


    @staticmethod
    def coupling_prompt(file: FileWithDependencies) -> str:
        code = PromptBuilder.build_code_bundle(file)
        return "\n".join([
            "You are a software engineer.",
            "You will be given one file with its file dependencies(possibly none).",
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
            "If no dependencies found and the main file has no coupling smells return single empty list.",
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

    
        # "After refactoring the main file and adding any new files, you must:",
        #     "- Review all dependency files for references to the main file’s class, methods, or fields.",
        #     "- Update those dependency files to reflect any renames, deletions, or new methods introduced in your refactor.",
        #     "- Ensure there are no invalid references in dependency files (such as calling a method that no longer exists).",
        #     "All updated dependency files should be included in your output alongside the main file and new files, following the Pydantic schema format.",

    @staticmethod
    def refactor_coupling_prompt(input_data: couplingSuggestionIn) -> str:
        print("input_data", input_data)
        code = PromptBuilder.build_coupling_code_bundle_refactor(input_data)
        print("code", code)
        return "\n".join([
            "You are an expert software engineer specialized in clean code and design principles like coupling, cohesion, and SOLID.",
            "You will be given:",
            "",
            "1. A list of files (each with its file path and file content).",
            "2. The detected coupling violations between these files — including which files are tightly coupled and how (especially: Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man).",
            "",
            "Your task is to:",
            "- Analyze the violations carefully.",
            "- Suggest **concise step-by-step refactoring solutions** for each violation without providing code.",
            "- Use design patterns (e.g., Dependency Injection, Observer, Interface Segregation) where relevant.",
            "- Avoid repeating the same general advice; be specific to the code structure I provide.",
            "",
            "Always respond in a structured JSON format. Do not include any explanation outside the JSON.",
            "You have to return the fixes according to the Pydantic schema below.",
            "Be objective and thorough, even if no suggestions are needed.",
            "Do not generate any introduction or conclusion.",
            "",
            "## files and the smells in between them:",
            json.dumps(code["coupling_smells"], ensure_ascii=False),
            "",
            "## Pydantic Details:",
            json.dumps(couplingSuggestionOut.model_json_schema(), ensure_ascii=False),
            "",
            "## Suggested Fixes:",
            "```json"
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
