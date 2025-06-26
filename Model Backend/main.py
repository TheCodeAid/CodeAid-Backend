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
    

# def extract_json_array_from_backticks(response: str):
#     """
#     Extracts the JSON array found between ```json and ``` backticks.
#     """

#     # Regex to find ```json followed by a JSON list then ```
#     match = re.search(r"```json\s*(\[.*?\])\s*```", response, re.DOTALL)
#     if not match:
#         raise ValueError("No JSON array found between ```json and ```.")

#     json_str = match.group(1).strip()

#     try:
#         return json.loads(json_str)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Failed to parse JSON: {e}")
    
    
    
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
            detection_result = coupling_handler.detect(f)
            if detection_result is None:
                print(f"Warning: detect returned None for file {f.mainFilePath}")
                coupling_violations = []
            else:
                # Ensure detection_result["couplingSmells"] is properly validated
                coupling_violations = extract_response(detection_result)
            print("coupling_violations", coupling_violations)
            if len(coupling_violations) == 0:
                print(f"No coupling violations detected for file {f.mainFilePath}")
                results.append({
                    "couplingSmells": []
                })
            # return[{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]
            # return [{"couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}]
            # return [{"filesPaths": ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], "couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}, {"filesPaths": ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\ShoppingCart.java'], "couplingSmells": [{'filesPaths': ['e:\\FCAI\\secondYear\\secondSemester\\sw\\Assignments\\ToffeeStore\\ToffeeStore\\ShoppingCart.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `displayItem()` and `displayItemForCart()` methods in the `item` class exhibit message chains by calling `category.getName()`. This forces the `item` class to navigate through its `category` object to get a name, coupling it to the internal structure of the `category` class.'}]}]}]
            else:
                results.append({
                    "couplingSmells": coupling_violations
                })
            # return [{'filesPaths': ['e:\\Documents\\GitHub\\Instapay_App\\out\\production\\Instapay_App1\\Account.java', 'e:\\Documents\\GitHub\\Instapay_App\\out\\production\\Instapay_App1\\ManagingSigning.java'], 'couplingSmells': [{'smell': 'Incomplete Library Class', 'justification': "Account's withdraw method directly calls DataBase's updateBalanceForSender with an ID, indicating missing functionality in DataBase. This forces Account to handle logic (finding the correct account) that should be encapsulated within DataBase, breaking encapsulation."}]}]
            # return [{'filesPaths': ['c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `category.displayCategoryItem()` method exhibits a message chain by calling `items.get(i).getCategory().getName()`. This forces the `category` class to navigate through `item` to `category` again to get the category name, violating the Law of Demeter.'}]}]
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
        refactored_files = solid_handler.refactorMainFile(files)
        if refactored_files is None:
            print(f"Warning: refactor returned None for file {files.data[0].mainFilePath}")
        else:
            mainfile_extracted_response = extract_response(refactored_files)
            try:
                validate_response(mainfile_extracted_response)
            except:
                print("Failed to validate refactored main file")
            for item in mainfile_extracted_response:
                refactoredCode.append(item)
            for entry in files.data:
                dependencies = entry.dependencies
                dependency_result = solid_handler.refactorDependencyFiles(files.data[0].mainFileContent, dependencies, mainfile_extracted_response)
                extracted_response = extract_response(dependency_result)
                try:
                    validate_response(extracted_response)
                except:
                    print("Failed to validate refactored dependency file")
                for item in extracted_response:
                    refactoredCode.append(item)

            # Ensure detection_result["couplingSmells"] is properly validated
            #refactoredCode = []
            # for item in extracted_response:
            #     try:
            #         validated_refactor = RefactoredFile(**item)
            #         refactoredCode.append(validated_refactor.model_dump())
            #     except Exception as ve:
            #         print(f"Validation failed for file {files.data[0].mainFilePath}: {ve}")
            #         continue
        print("refactoredCode", refactoredCode)
        return{  
            "refactored_files": refactoredCode
        }
        # return {
        #     "refactored_files": [{'filePath': 'e:Graduation Project\\TestExtension\\User\\User.java','fileContent':'package User;import Bill.Bill;import Transfer.*;import java.util.ArrayList;public abstract class User {    private final String username;    private final String password;    private final String phoneNo;    private Type type;    private final ArrayList<Transfer> Transfers;    private final ArrayList<Transfer> Recieved;    private final ArrayList<Bill> Bills;    public User(String username, String password, String phoneNo, Type type) {        this.username = username;        this.password = password;        this.phoneNo = phoneNo;        this.type = type;        this.Transfers = new ArrayList<>();        this.Recieved = new ArrayList<>();        this.Bills = new ArrayList<>();    }    public abstract boolean payBill(Bill bill);    public abstract void withdraw(double amount);    public abstract void deposit(double amount);    public abstract double getBalance();    public abstract String getSource();    public ArrayList<Bill> getBills() {        return Bills;    }    public ArrayList<Transfer> getTransfers() {        return Transfers;    }    public ArrayList<Transfer> getRecieved() {        return Recieved;    }    public Type getType() {        return type;    }    public String getUsername() {        return username;    }    public String getPhoneNo() {        return phoneNo;    }    public String getPassword() {        return password;    }    public void AddTransfer(Transfer t) {        Transfers.add(t);    }    public void ReceiveTransfer(Transfer t) {        Recieved.add(t);    }    public void AddBill(Bill b) {        Bills.add(b);    }}'},{'filePath': 'e:Graduation Project\\TestExtension\\User\\WalletUser.java','fileContent':'package User;import Bill.Bill;import Transfer.WalletTransfer;import Source.Wallet;public class WalletUser extends User {    Wallet wallet;    public WalletUser(String username, String password, String phoneNo, Type type, Wallet wallet) {        super(username, password, phoneNo, type);        this.wallet = wallet;    }    @Override    public void deposit(double amount) {        wallet.deposit(amount);    }    @Override    public double getBalance() {        return wallet.checkBalance();    }    @Override    public String getSource() {        return wallet.getPhoneNo();    }    @Override    public void withdraw(double amount) {        wallet.withdraw(amount);    }    @Override    public boolean payBill(Bill bill) {        if (bill.getAmount() < getBalance()) {            WalletTransfer utilTrans = new WalletTransfer(bill.getAmount(), this, bill.getReceiver());            if (utilTrans.transfer()) {                getBills().add(bill);                return bill.payBill();            }        }        return false;    }}'},{'filePath': 'e:Graduation Project\\TestExtension\\User\\BankUser.java','fileContent':'package User;import Bill.Bill;import Transfer.BankTransfer;import Source.Bank;public class BankUser extends User {    Bank bankCard;    public BankUser(String username, String password, String phoneNo, Type type, Bank card) {        super(username, password, phoneNo, type);        this.bankCard = card;    }    @Override    public double getBalance() {        return bankCard.checkBalance();    }    @Override    public String getSource() {        return bankCard.getCardNo();    }    @Override    public void withdraw(double amount) {        bankCard.withdraw(amount);    }    @Override    public void deposit(double amount) {        bankCard.deposit(amount);    }    @Override    public boolean payBill(Bill bill) {        if (bill.getAmount() < getBalance()) {            BankTransfer bankTrans = new BankTransfer(bill.getAmount(), this, bill.getReceiver());            if (bankTrans.transfer()) {                getBills().add(bill);                return bill.payBill();            }        }        return false;    }}'}]
        # }
    except Exception as e:
        print(f"Error processing file {files.data[0].mainFilePath}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing {files.data[0].mainFilePath}: {str(e)}"
        )
    return results



# @app.post("/refactor-coupling")
# def refactor_coupling(files: List[FileWithDependencies]):
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