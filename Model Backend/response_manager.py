from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import re
from models import CouplingViolationFix, FileWithDependencies, CouplingViolation, RefactoredFile, RefactoringRequestData, couplingSuggestionIn
from llm_client import LLMClient
from handlers.solid_handler import SolidHandler
from handlers.coupling_handler import CouplingHandler

class ResponseManager:
    def cleanContent(self, content: str) -> str:
        # 1. Remove actual escape characters (newline, tab, etc.)
        content = re.sub(r'[\n\r\t\f\v]', '', content)

        # 2. Remove any number of backslashes before letters n, r, t, f, v
        content = re.sub(r'(\\+)[nrtfv]', '', content)

        # 3. Collapse multiple spaces to one
        content = re.sub(r' {2,}', ' ', content)

        # 4. Trim leading/trailing spaces
        return content.strip()

    def extract_response(self, response: str):
        # Use regex to find content inside triple backticks
        match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", response)

        if not match:
            raise ValueError("Could not find JSON content between triple backticks.")

        json_part = match.group(1).strip()  # the content between ``` and ```

        # Try to parse the JSON
        try:
            violations = json.loads(json_part)
            print("Extracted JSON part:", violations)
            return violations
            # return [{'file_path': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on concrete item objects. High-level modules should depend on abstractions (interfaces) rather than concrete implementations to decouple dependencies.'}]}]
        except json.JSONDecodeError as e:
            print("\n\n\nresponse", response, "\n\n\n")
            raise ValueError("Failed to parse JSON from response.") from e

    def validate_response(self, refactored_files):
        result = []
        for item in refactored_files:
            try:
                validated_refactor = RefactoredFile(**item)
                result.append(validated_refactor.model_dump())
            except Exception as ve:
                print(f"Validation failed for file {item.filePath}: {ve}")
                continue
        return result
