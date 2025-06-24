from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

from models import FileWithDependencies, CouplingViolation, RefactoredFile, RefactoringRequestData
from llm_client import LLMClient
from handlers.solid_handler import SolidHandler
from handlers.coupling_handler import CouplingHandler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Initialize components
llm = LLMClient(api_url="https://fmcwkdag5o87x2ny.us-east-1.aws.endpoints.huggingface.cloud")
llmD = LLMClient(api_url="https://lbxfz9o9xa7fmfx6.us-east-1.aws.endpoints.huggingface.cloud")
llmR = LLMClient(api_url="")
solid_handler = SolidHandler(llmD, llmR)
coupling_handler = CouplingHandler(llm)


import json
import re

def extract_response(response: str):
    # Use regex to find content inside triple backticks
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", response)

    if not match:
        raise ValueError("Could not find JSON content between triple backticks.")

    json_part = match.group(1).strip()  # the content between ``` and ```

    # Try to parse the JSON
    try:
        violations = json.loads(json_part)
        print("Extracted JSON part:", violations)
        #return violations
        return [{'file_path': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on concrete item objects. High-level modules should depend on abstractions (interfaces) rather than concrete implementations to decouple dependencies.'}]}]
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse JSON from response.") from e
def extract_json_array_from_backticks(response: str):
    """
    Extracts the JSON array found between ```json and ``` backticks.
    """

    # Regex to find ```json followed by a JSON list then ```
    match = re.search(r"```json\s*(\[.*?\])\s*```", response, re.DOTALL)
    if not match:
        raise ValueError("No JSON array found between ```json and ```.")

    json_str = match.group(1).strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")
@app.post("/detect-solid")
def detect_solid(files: List[FileWithDependencies]):
    # print("Received files:", files)
    results = []
    for f in files:
        try:
            # detection_result = solid_handler.detect(f)
            # if detection_result is None:
            #     print(f"Warning: detect returned None for file {f.mainFilePath}")
            #     violations = []
            # else:
            #     violations = extract_response(detection_result)
            # results.append({
            #     "mainFilePath": f.mainFilePath,
            #     
            # "violations": violations
            # })
            return [{'mainFilePath': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violations': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on concrete item objects. High-level modules should depend on abstractions (interfaces) rather than concrete implementations to decouple dependencies.'}]}] 
        except Exception as e:
            print(f"Error processing file {f.mainFilePath}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {f.mainFilePath}: {str(e)}"
            )
    return results


@app.post("/detect-coupling")
def detect_coupling(files: List[FileWithDependencies]):
    results = []
    for f in files:
        try:
            # detection_result = coupling_handler.detect(f)
            # if detection_result is None:
            #     print(f"Warning: detect returned None for file {f.mainFilePath}")
            #     coupling_violations = []
            # else:
            #     # Ensure detection_result["couplingSmells"] is properly validated
            #     coupling_violations = extract_response(detection_result)
            # print("coupling_violations", coupling_violations)
            # results.append({
            #     "filesPaths": coupling_violations[0].get("filesPaths", []),
            #     "couplingSmells": smelling_violations[0].get("smells", [])
            # })
            return [{'filesPaths': ['c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `category.displayCategoryItem()` method exhibits a message chain by calling `items.get(i).getCategory().getName()`. This forces the `category` class to navigate through `item` to `category` again to get the category name, violating the Law of Demeter.'}]}]
        except Exception as e:
            print(f"Error processing file {f.mainFilePath}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {f.mainFilePath}: {str(e)}"
            )
    return results


@app.post("/refactor-solid")
def refactor_solid(files: RefactoringRequestData):
    print("Received files for refactoring:", files)
    results = []
    try:
        refactor_result = solid_handler.refactor(files)
        if refactor_result is None:
            print(f"Warning: refactor returned None for file {files.mainFilePath}")
            refactoredCode = []
        else:
            # Ensure detection_result["couplingSmells"] is properly validated
            refactoredCode = []
            for item in refactor_result.get("refactored_files", []):
                try:
                    validated_refactor = RefactoredFile(**item)
                    refactoredCode.append(validated_refactor.model_dump())
                except Exception as ve:
                    print(f"Validation failed for file {files.mainFilePath}: {ve}")
                    continue
        results.append({
            "refactored_files": refactoredCode
        })
    except Exception as e:
        print(f"Error processing file {files.mainFilePath}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing {files.mainFilePath}: {str(e)}"
        )
    return results



# @app.post("/refactor-coupling")
# def refactor_coupling(files: List[FileWithDependencies]):
#     return [{
#         "mainFilePath": f.mainFilePath,
#         "refactoredCode": coupling_handler.refactor(f).get("refactoredCode", "")
#     } for f in files]
