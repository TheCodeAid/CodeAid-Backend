from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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
llm = LLMClient(model_id="CodeAid/solid_model_v1")
solid_handler = SolidHandler(llm)
coupling_handler = CouplingHandler(llm)

@app.post("/detect-solid")
def detect_solid(files: List[FileWithDependencies]):
    # print("Received files:", files)
    results = []
    for f in files:
        try:
            detection_result = solid_handler.detect(f)
            if detection_result is None:
                print(f"Warning: detect returned None for file {f.mainFilePath}")
                violations = []
            else:
                violations = detection_result.get("violations", [])
            results.append({
                "mainFilePath": f.mainFilePath,
                "violations": violations
            })
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
            detection_result = coupling_handler.detect(f)
            if detection_result is None:
                print(f"Warning: detect returned None for file {f.mainFilePath}")
                coupling_violations = []
            else:
                # Ensure detection_result["couplingSmells"] is properly validated
                coupling_violations = []
                for item in detection_result.get("couplingSmells", []):
                    try:
                        validated_violation = CouplingViolation(**item)
                        coupling_violations.append(validated_violation.model_dump())
                    except Exception as ve:
                        print(f"Validation failed for file {f.mainFilePath}: {ve}")
                        continue
            results.append({
                "couplingSmells": coupling_violations
            })
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
