from pydantic import BaseModel, Field
from typing import List, Literal
class Dependency(BaseModel):
    depFilePath: str
    content: str

class FileWithDependencies(BaseModel):
    mainFilePath: str
    content: str
    dependencies: List[Dependency]

class ViolatedPrinciple(BaseModel):
    principle: str
    justification: str

Principle = Literal[
    # "Open-Closed"  "Open/Closed"
    "Single Responsibility", "Open-Closed", "Liskov",
    "Interface Segregation", "Dependency Inversion"
]

class ViolatedPrinciple(BaseModel):
    principle: Principle = Field(..., description="The violated SOLID principle.")
    justification: str = Field(..., max_length=300,
                               description="Explanation of why the principle was violated in 2 sentences only.")

class Violation(BaseModel):
    file_path: str = Field(..., description="Path of the file containing the violation.")
    violatedPrinciples: List[ViolatedPrinciple] = Field(...,
                                                        description="List of violated principles with justifications.")

class SolidDetectionOutput(BaseModel):
    violations: List[Violation] = Field(..., description="Detected SOLID violations.")

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

class RefactoringRequestData(BaseModel):
    mainFilePath: str
    content: str
    dependencies: List[Dependency]
    violations: List[ViolatedPrinciple] = Field(...,
                                                    description="List of violated principles with justifications.")



class RefactoredFile(BaseModel):
    filePath: str = Field(..., description="Path to the file either created or refactored.")
    fileContent: str = Field(..., description="The full content of the file")

class RefactoringOutput(BaseModel):
    refactored_files: List[RefactoredFile] = Field(..., description="List of all refactored files and their changes.")
