from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

from models import CouplingViolationFix, FileWithDependencies, CouplingViolation, RefactoredFile, RefactoringRequestData, couplingSuggestionIn
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
llmR = LLMClient(api_url="https://d1erunwqkqcxfcva.us-east-1.aws.endpoints.huggingface.cloud")
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
        return violations
        # return [{'file_path': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on concrete item objects. High-level modules should depend on abstractions (interfaces) rather than concrete implementations to decouple dependencies.'}]}]
    except json.JSONDecodeError as e:
        print("\n\n\nresponse", response, "\n\n\n")
        raise ValueError("Failed to parse JSON from response.") from e
    
def validate_response(refactored_files):
    result = []
    for item in refactored_files:
        try:
            validated_refactor = RefactoredFile(**item)
            result.append(validated_refactor.model_dump())
        except Exception as ve:
            print(f"Validation failed for file {item.filePath}: {ve}")
            continue
    return result
    
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
            # print("mainFile", f.mainFilePath)
            # print("violations", violations)
            # if len(violations) == 0:
            #     print(f"No SOLID violations detected for file {f.mainFilePath}")
            #     violations = []
            # else:
            #     # Ensure each violation is validated
            #     results.append({
            #         "mainFilePath": f.mainFilePath,
            #         "violations": violations
            #     })
            return [{"mainFilePath": f.mainFilePath, "violations":[{'file_path': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on the concrete item class. High-level modules should depend on abstractions rather than concrete implementations.'}]}]}]
            #return [{"mainFilePath": f.mainFilePath, "violations":[{'file_path': 'e:\\Graduation Project\\TestExtension\\User\\User.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on the concrete item class. High-level modules should depend on abstractions rather than concrete implementations.'}]}]}]
            # return [{'mainFilePath': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violations': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on concrete item objects. High-level modules should depend on abstractions (interfaces) rather than concrete implementations to decouple dependencies.'}]}] 

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
            # if len(coupling_violations) == 0:
            #     print(f"No coupling violations detected for file {f.mainFilePath}")
            #     results.append({
            #         "couplingSmells": []
            #     })
            # return[{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]
            # return [{"couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}]
            # return [{"filesPaths": ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], "couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}, {"filesPaths": ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\ShoppingCart.java'], "couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\ShoppingCart.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}]
            return [{"couplingSmells":  [{'filesPaths': ['c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `category.displayCategoryItem()` method exhibits a message chain by calling `items.get(i).getCategory().getName()`. This forces the `category` class to navigate through `item` to `category` again to get the category name, violating the Law of Demeter.'}]}]}]
            # else:
            #     results.append({
            #         "couplingSmells": coupling_violations
            #     })
            # return [{'filesPaths': ['e:\\Documents\\GitHub\\Instapay_App\\out\\production\\Instapay_App1\\Account.java', 'e:\\Documents\\GitHub\\Instapay_App\\out\\production\\Instapay_App1\\ManagingSigning.java'], 'couplingSmells': [{'smell': 'Incomplete Library Class', 'justification': "Account's withdraw method directly calls DataBase's updateBalanceForSender with an ID, indicating missing functionality in DataBase. This forces Account to handle logic (finding the correct account) that should be encapsulated within DataBase, breaking encapsulation."}]}]
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
    refactoredCode = []
    try:
        # refactored_files = solid_handler.refactorMainFile(files)
        # if refactored_files is None:
        #     print(f"Warning: refactor returned None for file {files.data[0].mainFilePath}")
        # else:
        #     mainfile_extracted_response = extract_response(refactored_files)
        #     try:
        #         validate_response(mainfile_extracted_response)
        #     except:
        #         print("Failed to validate refactored main file")
        #     for item in mainfile_extracted_response:
        #         refactoredCode.append(item)
        #     for entry in files.data:
        #         dependencies = entry.dependencies
        #         dependency_result = solid_handler.refactorDependencyFiles(files.data[0].mainFileContent, dependencies, mainfile_extracted_response)
        #         extracted_response = extract_response(dependency_result)
        #         try:
        #             validate_response(extracted_response)
        #         except:
        #             print("Failed to validate refactored dependency file")
        #         for item in extracted_response:
        #             refactoredCode.append(item)

        #     # Ensure detection_result["couplingSmells"] is properly validated
        #     #refactoredCode = []
        #     # for item in extracted_response:
        #     #     try:
        #     #         validated_refactor = RefactoredFile(**item)
        #     #         refactoredCode.append(validated_refactor.model_dump())
        #     #     except Exception as ve:
        #     #         print(f"Validation failed for file {files.data[0].mainFilePath}: {ve}")
        #     #         continue
        # print("refactoredCode", refactoredCode)
        # return{  
        #     "refactored_files": refactoredCode
        # }
        return {
        "refactored_files": [{'filePath': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'fileContent': 'import java.util.ArrayList;\nimport java.util.List;\n\npublic class category {\n  private String name;\n  private List<item> items;\n  private String description;\n\n  public category() {\n    this.items = new ArrayList<>();\n  }\n\n  public String getName() {\n    return name;\n  }\n\n  public void setName(String name) {\n    this.name = name;\n  }\n\n  public int counter() {\n    return items.size();\n  }\n\n  public List<item> getItems() {\n    return items;\n  }\n\n  public void addItem(item item) {\n    items.add(item);\n  }\n}'}, {'filePath': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\CategoryDisplay.java', 'fileContent': 'import java.io.IOException;\nimport java.util.List;\n\npublic class CategoryDisplay {\n\n  public void displayCategoryItems(category category) throws IOException {\n    System.out.println("\\n^^^^^^^^^" + category.getName() + " CATEGORY" + "^^^^^^^^^");\n    for (item item : category.getItems()) {\n      System.out.println();\n      System.out.println("Name: " + item.getName());\n      System.out.println("Category: " + item.getCategory().getName());\n      System.out.println("Brand: " + item.getBrand());\n      System.out.println("Price: " + item.getPrice());\n      System.out.println();\n    }\n  }\n}'}, {'filePath': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\item.java', 'fileContent': 'import java.util.jar.Attributes.Name;\n\nimport javax.sound.sampled.AudioFileFormat.Type;\n\npublic class item {\n    private String name;\n    private String brand;\n    private category category;\n    double availablenum;\n    private double price;\n    String description;\n    double maxQuantity;\n    double orderedQuantity;\n    String itemType;\n\n    public item() {\n    }\n\n    public void setName(String name) {\n        this.name = name;\n    }\n\n    public String getName() {\n        return name;\n    }\n\n    public void setBrand(String brand) {\n        this.brand = brand;\n    }\n\n    public String getBrand() {\n        return brand;\n    }\n\n    public void setCategory(category category) {\n        this.category = category;\n    }\n\n    public category getCategory() {\n        return category;\n    }\n\n    public void setAvailableNum(double amount) {\n        this.availablenum = amount;\n    }\n\n    public double getAvailableNum() {\n        return availablenum;\n    }\n\n    public void setDescription(String desc) {\n        this.description = desc;\n    }\n\n    public String getDescription() {\n        return description;\n\n    }\n\n    public void setPrice(double p) {\n        this.price = p;\n    }\n\n    public double getPrice() {\n        return price;\n    }\n\n    public void setMaxQuantity(double max) {\n        this.maxQuantity = max;\n    }\n\n    public double getMaxQuantity() {\n        return maxQuantity;\n    }\n\n    public void setOrderedQuantity(double quantity) {\n        this.orderedQuantity = quantity;\n    }\n\n    public double getOrderedQuantity() {\n        return orderedQuantity;\n    }\n\n    public void setIemType(String type) {\n        itemType = type;\n    }\n\n    public String getItemType() {\n        return itemType;\n    }\n\n    public void displayItem() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Price : " + price);\n        System.out.println("");\n    }\n\n    public void displayItemForCart() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Ordered Quantity : " + orderedQuantity);\n        System.out.println(" Unit : " + itemType);\n        System.out.println(" Price : " + price);\n        System.out.println("");\n    }\n\n}'}] 
                }
    except Exception as e:
        print(f"Error processing file {files.data[0].mainFilePath}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing {files.data[0].mainFilePath}: {str(e)}"
        )
    return results



@app.post("/refactor-coupling")
def refactor_coupling(file: couplingSuggestionIn):
    print("Received files for refactoring:", file)
    results = []
    suggestions = []
    try:
        suggestions = coupling_handler.refactor(file)
        if suggestions is None:
            print(f"Warning: refactor returned None for file {file.coupling_smells[0].files[0].filePath}")
        else:
            # Ensure suggestions["suggestions"] is properly validated
            suggestions = extract_response(suggestions)
            for item in suggestions.get("suggestions", []):
                print("item", item)
                try:
                    validated_suggestion = CouplingViolationFix(**item)
                    results.append(validated_suggestion.model_dump())
                except Exception as ve:
                    print(f"Validation failed for file")
                    continue
    except Exception as e:
        print(f"Error processing file {file.coupling_smells[0].files[0].filePath}: {str(e)}")
        raise HTTPException(    
            status_code=500,
            detail=f"Error processing {file.coupling_smells[0].files[0].filePath}: {str(e)}"
        )
    return {
        "suggestions": results
    }
#     return [{
#         "mainFilePath": f.mainFilePath,
#         "refactoredCode": coupling_handler.refactor(f).get("refactoredCode", "")
#     } for f in files]


# for item in detection_result.get("couplingSmells", []):
#                     # try:
#                     #     validated_violation = CouplingViolation(**item)
#                     #     coupling_violations.append(validated_violation.model_dump())
#                     # except Exception as ve:
#                     #     print(f"Validation failed for file {f.mainFilePath}: {ve}")
#                     #     continu