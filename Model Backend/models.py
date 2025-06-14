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
