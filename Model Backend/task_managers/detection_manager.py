from typing import List
import json
from fastapi import HTTPException
from models import CouplingViolationFix, FileWithDependencies, CouplingViolation, RefactoredFile, RefactoringRequestData, couplingSuggestionIn
from llm_client import LLMClient
from handlers.solid_handler import SolidHandler
from handlers.coupling_handler import CouplingHandler

class DetectionManager:
    def __init__(self, solid_handler, coupling_handler, response_manager):
        self.solid_handler = solid_handler
        self.coupling_handler = coupling_handler
        self.response_manager = response_manager

    def detect_solid(self, files: List[FileWithDependencies]):
        results = []
        for f in files:
            try:
                detection_result = self.solid_handler.detect(f)
                if detection_result is None:
                    print(f"Warning: detect returned None for file {f.mainFilePath}")
                    violations = []
                else:
                    violations = self.response_manager.extract_response(detection_result)
                print("mainFile", f.mainFilePath)
                print("violations", violations)
                if len(violations) == 0:
                    print(f"No SOLID violations detected for file {f.mainFilePath}")
                else:
                    results.append({
                        "mainFilePath": f.mainFilePath,
                        "violations": violations
                    })
                print("returning")

                # return [{
                #     "mainFilePath": f.mainFilePath,
                #     "violations": [{
                #         'file_path': f.mainFilePath,
                #         'violatedPrinciples':[
                #             {
                #                 'principle': 'Single Responsibility',
                #                 'justification': 'The Database class handles multiple responsibilities: user registration validation, file I/O operations, order management, inventory updates, and authentication. This violates SRP as changes in any of these areas would require modifying the same class.'
                #             },
                #             {
                #                 'principle': 'Open-Closed',
                #                 'justification': 'The class directly implements file operations and validation logic without abstractions. Adding new validation rules or storage mechanisms would require modifying existing methods rather than extending through new classes.'
                #             }
                #         ]
                #     }]
                # }]
                
                # return [{"mainFilePath": f.mainFilePath, "violations": [{
                #     'file_path': f.mainFilePath,
                #     'violatedPrinciples': [
                #         {'principle': 'Single Responsibility',
                #          'justification': 'PostServiceImpl handles multiple responsibilities: business logic for post operations, direct data access coordination, and DTO-entity mapping. This creates multiple reasons for the class to change.'},
                #         {'principle': 'Dependency Inversion',
                #          'justification': 'PostServiceImpl directly depends on concrete ModelMapper implementation instead of an abstraction. High-level service modules should depend on abstractions for mapping, not concrete third-party classes.'}]}]}]

            except Exception as e:
                print(f"Error processing file {f.mainFilePath}: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing {f.mainFilePath}: {str(e)}"
                )
        return results

    def detect_coupling(self, files: List[FileWithDependencies]):
        results = []
        for f in files:
            try:
                detection_result = self.coupling_handler.detect(f)
                print("raw detection", detection_result)
                if detection_result is None:
                    print(f"Warning: detect returned None for file {f.mainFilePath}")
                    coupling_violations = []
                else:
                    coupling_violations = self.response_manager.extract_response(detection_result)
                print("coupling_violations", coupling_violations)
                results.append({
                    "mainFilePath": f.mainFilePath,
                    "couplingSmells": coupling_violations
                })
                # return[{'filesPaths': ['e:\\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]
            except Exception as e:
                print(f"Error processing file {f.mainFilePath}: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing {f.mainFilePath}: {str(e)}"
                )
        return results
