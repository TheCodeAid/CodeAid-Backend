from pydantic import BaseModel, Field
from typing import List, Literal
class Dependency(BaseModel):
    depFilePath: str
    depFileContent: str

class FileWithDependencies(BaseModel):
    project_id: str
    chunk_id: int
    mainFilePath: str
    mainFileContent: str
    dependencies: List[Dependency]



Principle = Literal[
    "Single Responsibility", "Open-Closed", "Liskov",
    "Interface Segregation", "Dependency Inversion"
]

class ViolatedPrinciple(BaseModel):
    principle: Principle = Field(..., description="The violated SOLID principle.")
    justification: str = Field(..., max_length=300,
                               description="Explanation of why the principle was violated in 2 sentences only.")
class ViolatedPrincipleR(BaseModel):
    principle: Principle
    justification: str

class Violation(BaseModel):
    file_path: str = Field(..., description="Path of the file containing the violation.")
    violatedPrinciples: List[ViolatedPrinciple] = Field(...,
                                                        description="List of violated principles with justifications.")

class SolidDetectionOutput(BaseModel):
    violations: List[Violation] = Field(..., description="Detected SOLID violations.")

class RefactoredFile(BaseModel):
    filePath: str = Field(..., description="Path to the file either created or refactored.")
    fileContent: str = Field(..., description="The full content of the file")

class RefactoringOutput(BaseModel):
    refactored_files: List[RefactoredFile] = Field(..., description="List of all refactored files and their changes.")



Smell = Literal[
    "Feature Envy", "Inappropriate Intimacy",
    "Message Chains", "Middle Man"
]

class CouplingSmell(BaseModel):
    smell: Smell = Field(..., description="Type of coupling smell detected.")
    justification: str = Field(..., max_length=300,
                               description="Justification for the detected coupling smell in 2 sentences only.")
class CouplingViolation(BaseModel):
    filesPaths: List[str] = Field(..., description="Files involved in the coupling smell.")
    smells: List[CouplingSmell] = Field(..., description="Details about the detected coupling smells.")
    
class CouplingDetectionOutput(BaseModel):
    couplingSmells: List[CouplingViolation] = Field(..., description="Detected coupling code smells.")

class RefactoringWrappedData(BaseModel):
    project_id: str
    chunk_id: int
    mainFilePath: str
    mainFileContent: str
    dependents: List[Dependency]

class RefactoringRequestData(BaseModel):
    data: List[RefactoringWrappedData]
    violations: List[ViolatedPrincipleR] = Field(...,
                                                    description="List of violated principles with justifications.")


# input pydantics 
class file(BaseModel):
    filePath: str  # Path to the file
    content: str  # Content of the file

class smell(BaseModel):
    smell: str  # Type of coupling smell (e.g., "Message Chains")
    justification: str  # Justification for the smell

class CouplingViolations(BaseModel):
    files: List[file]  # List of file dictionaries with filePath and fileContent
    smells: List[smell]  # List of detected coupling smells with smell type and justification

class couplingSuggestionIn(BaseModel):
    coupling_smells: List[CouplingViolations]

#output pydantics
class CouplingViolationFix(BaseModel):
    smell: str
    files_involved: List[str]
    suggested_steps: List[str]

class couplingSuggestionOut(BaseModel):
    suggestions: List[CouplingViolationFix]


