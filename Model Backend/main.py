from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import CouplingViolationFix, FileWithDependencies, RefactoringRequestData, couplingSuggestionIn
from llm_client import LLMClient
from handlers.solid_handler import SolidHandler
from handlers.coupling_handler import CouplingHandler
from response_manager import ResponseManager
from task_managers.refactoring_manager import RefactoringManager
from task_managers.detection_manager import DetectionManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Initialize components
llm = LLMClient(api_url="https://mrtlyk6k6fnajdmf.us-east-1.aws.endpoints.huggingface.cloud")
llmD = LLMClient(api_url="https://lbxfz9o9xa7fmfx6.us-east-1.aws.endpoints.huggingface.cloud")
#https://d1erunwqkqcxfcva.us-east-1.aws.endpoints.huggingface.cloud
#https://n93vhujiweb948st.us-east-1.aws.endpoints.huggingface.cloud
llmR = LLMClient(api_url="https://n93vhujiweb948st.us-east-1.aws.endpoints.huggingface.cloud")
solid_handler = SolidHandler(llmD, llmR)
coupling_handler = CouplingHandler(llm)
response_manager = ResponseManager()
refactor_manager = RefactoringManager(solid_handler, coupling_handler, response_manager)
detection_manager = DetectionManager(solid_handler, coupling_handler, response_manager)



@app.post("/detect-solid")
def detect_solid(files: List[FileWithDependencies]):
    try:
        return detection_manager.detect_solid(files)
    except Exception as e:
        print("Error in detect_solid:", e)
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/detect-coupling")
def detect_coupling(files: List[FileWithDependencies]):
    try:
        return detection_manager.detect_coupling(files)
    except Exception as e:
        print("Error in detect_solid:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/refactor-solid")
def refactor_solid(files: RefactoringRequestData):
    try:
        return refactor_manager.refactor_solid(files)
    except Exception as e:
        print("Error in detect_solid:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/refactor-coupling")
def refactor_coupling(file: couplingSuggestionIn):
    try:
        return refactor_manager.refactor_coupling(file)
    except Exception as e:
        print("Error in detect_solid:", e)
        raise HTTPException(status_code=500, detail=str(e))
    