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


import re

def cleanContent(content: str) -> str:
    # 1. Remove actual escape characters (newline, tab, etc.)
    content = re.sub(r'[\n\r\t\f\v]', '', content)

    # 2. Remove any number of backslashes before letters n, r, t, f, v
    content = re.sub(r'(\\+)[nrtfv]', '', content)

    # 3. Collapse multiple spaces to one
    content = re.sub(r' {2,}', ' ', content)

    # 4. Trim leading/trailing spaces
    return content.strip()


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
            return [{"mainFilePath": f.mainFilePath, "violations": [{'file_path': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\service\\impl\\PostServiceImpl.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'PostServiceImpl handles multiple responsibilities: business logic for post operations, direct data access coordination, and DTO-entity mapping. This creates multiple reasons for the class to change.'}, {'principle': 'Dependency Inversion', 'justification': 'PostServiceImpl directly depends on concrete ModelMapper implementation instead of an abstraction. High-level service modules should depend on abstractions for mapping, not concrete third-party classes.'}]}]}]
            # return [{"mainFilePath": f.mainFilePath, "violations": [{'file_path': 'c:\\Users\\Mariam\\OneDrive\\Documents\\GitHub\\Toffee\\Order.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The Order class handles multiple responsibilities: managing order data, calculating total price, and maintaining product mappings. These distinct functionalities should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The Order class directly depends on the concrete Product class in its map (OProducts). High-level modules should depend on abstractions rather than concrete implementations.'}]}, {'file_path': 'c:\\Users\\Mariam\\OneDrive\\Documents\\GitHub\\Toffee\\Product.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The Product class includes a constructor that directly interacts with the Catalog class, combining product data management with data retrieval logic. This dual responsibility violates SRP.'}, {'principle': 'Dependency Inversion', 'justification': 'The Product class directly depends on the concrete Catalog class in one of its constructors. Low-level modules should implement abstractions rather than being directly referenced.'}]}]}]
            # return [{"mainFilePath": f.mainFilePath, "violations":[{'file_path': 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on the concrete item class. High-level modules should depend on abstractions rather than concrete implementations.'}]}]}]
            # return [{"mainFilePath": f.mainFilePath, "violations":[{'file_path': 'e:\\Graduation Project\\TestExtension\\User\\User.java', 'violatedPrinciples': [{'principle': 'Single Responsibility', 'justification': 'The category class handles both data management (storing items) and presentation logic (displayCategoryItem method). These are two distinct responsibilities that should be separated into different classes.'}, {'principle': 'Dependency Inversion', 'justification': 'The displayCategoryItem method directly depends on the concrete item class. High-level modules should depend on abstractions rather than concrete implementations.'}]}]}]
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
            # return [{"couplingSmells":  [{'filesPaths': ['c:\\Users\\marwa\\Downloads\\ToffeeStore\\category.java', 'c:\\Users\\marwa\\Downloads\\ToffeeStore\\item.java'], 'smells': [{'smell': 'Message Chains', 'justification': 'The `category.displayCategoryItem()` method exhibits a message chain by calling `items.get(i).getCategory().getName()`. This forces the `category` class to navigate through `item` to `category` again to get the category name, violating the Law of Demeter.'}]}]}]
            else:
                results.append({
                    "couplingSmells": coupling_violations
                })
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
    # print("Received files for refactoring:", files)
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
        #         cleanedContent = cleanContent(item.get("fileContent"))
        #         # print(cleanedContent)
        #         refactoredCode.append({
        #             "filePath": item.get("filePath"),
        #             "fileContent": cleanedContent
        #         })
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
        # print("\n\n\n\n\nrefactoredCode\n\n\n\n\n", refactoredCode)
        # return{
        #     "refactored_files": refactoredCode
        # }
        # return {
        #     "refactored_files":[{'filePath':'e:Graduation Project\\TestExtension\\User\\User.java','fileContent':'package User;import Bill.Bill;import Transfer.*;import java.util.ArrayList;public abstract class User {    private final String username;    private final String password;    private final String phoneNo;    private Type type;    private final ArrayList<Transfer> Transfers;    private final ArrayList<Transfer> Recieved;    private final ArrayList<Bill> Bills;    public User(String username, String password, String phoneNo, Type type) {        this.username = username;        this.password = password;        this.phoneNo = phoneNo;        this.type = type;        this.Transfers = new ArrayList<>();        this.Recieved = new ArrayList<>();        this.Bills = new ArrayList<>();    }    public abstract boolean payBill(Bill bill);    public abstract void withdraw(double amount);    public abstract void deposit(double amount);    public abstract double getBalance();    public abstract String getSource();    public ArrayList<Bill> getBills() {        return Bills;    }    public ArrayList<Transfer> getTransfers() {        return Transfers;    }    public ArrayList<Transfer> getRecieved() {        return Recieved;    }    public Type getType() {        return type;    }    public String getUsername() {        return username;    }    public String getPhoneNo() {        return phoneNo;    }    public String getPassword() {        return password;    }    public void AddTransfer(Transfer t) {        Transfers.add(t);    }    public void ReceiveTransfer(Transfer t) {        Recieved.add(t);    }    public void AddBill(Bill b) {        Bills.add(b);    }}'},{'filePath':'e:Graduation Project\\TestExtension\\User\\WalletUser.java','fileContent':'package User;import Bill.Bill;import Transfer.WalletTransfer;import Source.Wallet;public class WalletUser extends User {    Wallet wallet;    public WalletUser(String username, String password, String phoneNo, Type type, Wallet wallet) {        super(username, password, phoneNo, type);        this.wallet = wallet;    }    @Override    public void deposit(double amount) {        wallet.deposit(amount);    }    @Override    public double getBalance() {        return wallet.checkBalance();    }    @Override    public String getSource() {        return wallet.getPhoneNo();    }    @Override    public void withdraw(double amount) {        wallet.withdraw(amount);    }    @Override    public boolean payBill(Bill bill) {        if (bill.getAmount() < getBalance()) {            WalletTransfer utilTrans = new WalletTransfer(bill.getAmount(), this, bill.getReceiver());            if (utilTrans.transfer()) {                getBills().add(bill);                return bill.payBill();            }        }        return false;    }}'},{'filePath':'e:Graduation Project\\TestExtension\\User\\BankUser.java','fileContent':'package User;import Bill.Bill;import Transfer.BankTransfer;import Source.Bank;public class BankUser extends User {    Bank bankCard;    public BankUser(String username, String password, String phoneNo, Type type, Bank card) {        super(username, password, phoneNo, type);        this.bankCard = card;    }    @Override    public double getBalance() {        return bankCard.checkBalance();    }    @Override    public String getSource() {        return bankCard.getCardNo();    }    @Override    public void withdraw(double amount) {        bankCard.withdraw(amount);    }    @Override    public void deposit(double amount) {        bankCard.deposit(amount);    }    @Override    public boolean payBill(Bill bill) {        if (bill.getAmount() < getBalance()) {            BankTransfer bankTrans = new BankTransfer(bill.getAmount(), this, bill.getReceiver());            if (bankTrans.transfer()) {                getBills().add(bill);                return bill.payBill();            }        }        return false;    }}'},{'filePath': 'e:\\Graduation Project\\TestExtension\\User\\item.java', 'fileContent': 'import java.util.jar.Attributes.Name;\n\nimport javax.sound.sampled.AudioFileFormat.Type;\n\npublic class item {\n    private String name;\n    private String brand;\n    private category category;\n    double availablenum;\n    private double price;\n    String description;\n    double maxQuantity;\n    double orderedQuantity;\n    String itemType;\n\n    public item() {\n    }\n\n    public void setName(String name) {\n        this.name = name;\n    }\n\n    public String getName() {\n        return name;\n    }\n\n    public void setBrand(String brand) {\n        this.brand = brand;\n    }\n\n    public String getBrand() {\n        return brand;\n    }\n\n    public void setCategory(category category) {\n        this.category = category;\n    }\n\n    public category getCategory() {\n        return category;\n    }\n\n    public void setAvailableNum(double amount) {\n        this.availablenum = amount;\n    }\n\n    public double getAvailableNum() {\n        return availablenum;\n    }\n\n    public void setDescription(String desc) {\n        this.description = desc;\n    }\n\n    public String getDescription() {\n        return description;\n\n    }\n\n    public void setPrice(double p) {\n        this.price = p;\n    }\n\n    public double getPrice() {\n        return price;\n    }\n\n    public void setMaxQuantity(double max) {\n        this.maxQuantity = max;\n    }\n\n    public double getMaxQuantity() {\n        return maxQuantity;\n    }\n\n    public void setOrderedQuantity(double quantity) {\n        this.orderedQuantity = quantity;\n    }\n\n    public double getOrderedQuantity() {\n        return orderedQuantity;\n    }\n\n    public void setIemType(String type) {\n        itemType = type;\n    }\n\n    public String getItemType() {\n        return itemType;\n    }\n\n    public void displayItem() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Price : " + price);\n        System.out.println(");\n    }\n\n    public void displayItemForCart() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Ordered Quantity : " + orderedQuantity);\n        System.out.println(" Unit : " + itemType);\n        System.out.println(" Price : " + price);\n        System.out.println("");\n    }\n\n}'}]
        # }
        # return {
        # "refactored_files": [{'filePath': 'e:\\Graduation Project\\TestExtension\\User\\User.java', 'fileContent': 'import java.util.ArrayList;\nimport java.util.List;\n\npublic class category {\n  private String name;\n  private List<item> items;\n  private String description;\n\n  public category() {\n    this.items = new ArrayList<>();\n  }\n\n  public String getName() {\n    return name;\n  }\n\n  public void setName(String name) {\n    this.name = name;\n  }\n\n  public int counter() {\n    return items.size();\n  }\n\n  public List<item> getItems() {\n    return items;\n  }\n\n  public void addItem(item item) {\n    items.add(item);\n  }\n}'}, {'filePath': 'e:\\Graduation Project\\TestExtension\\User\\CategoryDisplay.java', 'fileContent': 'import java.io.IOException;\nimport java.util.List;\n\npublic class CategoryDisplay {\n\n  public void displayCategoryItems(category category) throws IOException {\n    System.out.println("\\n^^^^^^^^^" + category.getName() + " CATEGORY" + "^^^^^^^^^");\n    for (item item : category.getItems()) {\n      System.out.println();\n      System.out.println("Name: " + item.getName());\n      System.out.println("Category: " + item.getCategory().getName());\n      System.out.println("Brand: " + item.getBrand());\n      System.out.println("Price: " + item.getPrice());\n      System.out.println();\n    }\n  }\n}'}, {'filePath': 'e:\\Graduation Project\\TestExtension\\User\\item.java', 'fileContent': 'import java.util.jar.Attributes.Name;\n\nimport javax.sound.sampled.AudioFileFormat.Type;\n\npublic class item {\n    private String name;\n    private String brand;\n    private category category;\n    double availablenum;\n    private double price;\n    String description;\n    double maxQuantity;\n    double orderedQuantity;\n    String itemType;\n\n    public item() {\n    }\n\n    public void setName(String name) {\n        this.name = name;\n    }\n\n    public String getName() {\n        return name;\n    }\n\n    public void setBrand(String brand) {\n        this.brand = brand;\n    }\n\n    public String getBrand() {\n        return brand;\n    }\n\n    public void setCategory(category category) {\n        this.category = category;\n    }\n\n    public category getCategory() {\n        return category;\n    }\n\n    public void setAvailableNum(double amount) {\n        this.availablenum = amount;\n    }\n\n    public double getAvailableNum() {\n        return availablenum;\n    }\n\n    public void setDescription(String desc) {\n        this.description = desc;\n    }\n\n    public String getDescription() {\n        return description;\n\n    }\n\n    public void setPrice(double p) {\n        this.price = p;\n    }\n\n    public double getPrice() {\n        return price;\n    }\n\n    public void setMaxQuantity(double max) {\n        this.maxQuantity = max;\n    }\n\n    public double getMaxQuantity() {\n        return maxQuantity;\n    }\n\n    public void setOrderedQuantity(double quantity) {\n        this.orderedQuantity = quantity;\n    }\n\n    public double getOrderedQuantity() {\n        return orderedQuantity;\n    }\n\n    public void setIemType(String type) {\n        itemType = type;\n    }\n\n    public String getItemType() {\n        return itemType;\n    }\n\n    public void displayItem() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Price : " + price);\n        System.out.println("");\n    }\n\n    public void displayItemForCart() {\n        System.out.println(" Name : " + name);\n        System.out.println(" Category : " + category.getName());\n        System.out.println(" Brand : " + brand);\n        System.out.println(" Ordered Quantity : " + orderedQuantity);\n        System.out.println(" Unit : " + itemType);\n        System.out.println(" Price : " + price);\n        System.out.println("");\n    }\n\n}'}] 
        #         }
        return{
            "refactored_files": [
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\service\\impl\\PostServiceImpl.java',
                    'fileContent': 'package com.suraj.blog.service.impl;import java.util.Date;import java.util.List;import java.util.stream.Collectors;import org.modelmapper.ModelMapper;import org.springframework.beans.factory.annotation.Autowired;import org.springframework.data.domain.Page;import org.springframework.data.domain.PageRequest;import org.springframework.data.domain.Pageable;import org.springframework.data.domain.Sort;import org.springframework.stereotype.Service;import com.suraj.blog.dao.CategoryRepo;import com.suraj.blog.dao.PostRepo;import com.suraj.blog.dao.UserRepo;import com.suraj.blog.entity.Category;import com.suraj.blog.entity.Post;import com.suraj.blog.entity.User;import com.suraj.blog.exceptions.ResourceNotFoundException;import com.suraj.blog.payload.PostDto;import com.suraj.blog.service.PostService;import com.suraj.blog.service.PostMapper;@Servicepublic class PostServiceImpl implements PostService {@Autowiredprivate PostRepo postRepo;@Autowiredprivate UserRepo userRepo;@Autowiredprivate CategoryRepo categoryRepo;@Autowiredprivate PostMapper postMapper;@Overridepublic PostDto createPost(PostDto postDto, Integer userId, Integer categoryId) {User user = this.userRepo.findById(userId).orElseThrow(() -> new ResourceNotFoundException("User", "userId", userId));Category category = this.categoryRepo.findById(categoryId).orElseThrow(() -> new ResourceNotFoundException("Category", "categoryId", categoryId));Post post = postMapper.toEntity(postDto);post.setImageName("default.png");post.setAddedDate(new Date());post.setUser(user);post.setCategory(category);Post newPost = this.postRepo.save(post);return postMapper.toDto(newPost);}@Overridepublic PostDto updatePost(PostDto postDto, Integer postId) {Post post = this.postRepo.findById(postId).orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));postMapper.update(post, postDto);Post updatedPost = this.postRepo.save(post);return postMapper.toDto(updatedPost);}@Overridepublic void deletePost(Integer postId) {Post post = this.postRepo.findById(postId).orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));this.postRepo.delete(post);}@Overridepublic List<PostDto> getAllPost(Integer pageNumber, Integer pageSize, String sortBy, String sortDir) {Sort sort = null;if(sortDir.equalsIgnoreCase("a")) {sort = Sort.by(sortBy).ascending();}else { sort = Sort.by(sortBy).descending();}Pageable p = PageRequest.of(pageNumber, pageSize, sort);Page<Post> page = this.postRepo.findAll(p);List<Post> posts = page.getContent();List<PostDto> postDtos = posts.stream().map(postMapper::toDto).collect(Collectors.toList());return postDtos;}@Overridepublic PostDto getPostById(Integer postId) {Post post = this.postRepo.findById(postId).orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));return postMapper.toDto(post);}@Overridepublic List<PostDto> getPostByCategory(Integer categoryId) {Category category = this.categoryRepo.findById(categoryId).orElseThrow(() -> new ResourceNotFoundException("Category", "categoryId", categoryId));List<Post> posts = this.postRepo.findByCategory(category);List<PostDto> postDtos = posts.stream().map(postMapper::toDto).collect(Collectors.toList());return postDtos;}@Overridepublic List<PostDto> getPostByUser(Integer userId) {User user = this.userRepo.findById(userId).orElseThrow(() -> new ResourceNotFoundException("User", "userId", userId));List<Post> posts = this.postRepo.findByUser(user);List<PostDto> postDtos = posts.stream().map(postMapper::toDto).collect(Collectors.toList());return postDtos;}@Overridepublic List<PostDto> searchPosts(String Keyword) {List<Post> posts = this.postRepo.findByTitleContaining(Keyword);List<PostDto> postDtos = posts.stream().map(postMapper::toDto).collect(Collectors.toList());return postDtos;}}'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\service\\PostMapper.java',
                    'fileContent': 'package com.suraj.blog.service;import org.modelmapper.ModelMapper;import org.springframework.beans.factory.annotation.Autowired;import org.springframework.stereotype.Component;import com.suraj.blog.entity.Post;import com.suraj.blog.payload.PostDto;@Componentpublic class PostMapper {@Autowiredprivate ModelMapper modelMapper;public Post toEntity(PostDto postDto) {return modelMapper.map(postDto, Post.class);}public PostDto toDto(Post post) {return modelMapper.map(post, PostDto.class);}public void update(Post post, PostDto postDto) {post.setTitle(postDto.getTitle());post.setContent(postDto.getContent());post.setImageName(postDto.getImageName());}}'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\dao\\CategoryRepo.java',
                    'fileContent': 'package com.suraj.blog.dao;\\n\\nimport org.springframework.data.jpa.repository.JpaRepository;\\n\\nimport com.suraj.blog.entity.Category;\\n\\npublic interface CategoryRepo extends JpaRepository<Category, Integer> {\\n\t\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\dao\\PostRepo.java',
                    'fileContent': 'package com.suraj.blog.dao;\\n\\nimport java.util.List;\\n\\nimport org.springframework.data.jpa.repository.JpaRepository;\\n\\nimport com.suraj.blog.entity.Category;\\nimport com.suraj.blog.entity.Post;\\nimport com.suraj.blog.entity.User;\\n\\npublic interface PostRepo extends JpaRepository<Post, Integer> {\\n\tList<Post> findByUser(User user);\\n\\n\tList<Post> findByCategory(Category category);\\n\t\\n\tList<Post> findByTitleContaining(String title);\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\dao\\UserRepo.java',
                    'fileContent': 'package com.suraj.blog.dao;\\n\\nimport org.springframework.data.jpa.repository.JpaRepository;\\n\\nimport com.suraj.blog.entity.User;\\n\\npublic interface UserRepo extends JpaRepository<User, Integer> {\\n\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\entity\\Category.java',
                    'fileContent': 'package com.suraj.blog.entity;\\n\\nimport java.util.ArrayList;\\nimport java.util.List;\\n\\nimport javax.persistence.CascadeType;\\nimport javax.persistence.Column;\\nimport javax.persistence.Entity;\\nimport javax.persistence.FetchType;\\nimport javax.persistence.GeneratedValue;\\nimport javax.persistence.GenerationType;\\nimport javax.persistence.Id;\\nimport javax.persistence.OneToMany;\\n\\nimport lombok.AllArgsConstructor;\\nimport lombok.Getter;\\nimport lombok.NoArgsConstructor;\\nimport lombok.Setter;\\n\\n@Entity\\n@Getter\\n@Setter\\n@NoArgsConstructor\\n@AllArgsConstructor\\npublic class Category {\\n\\n\t@Id\\n\t@GeneratedValue(strategy = GenerationType.IDENTITY)\\n\tprivate Integer categoryId;\\n\t@Column(name = "title", length = 100, nullable =false) \\n\tprivate String categoryTitle;\\n\t@Column(name = "description")\\n\tprivate String categoryDescription;\\n\t\\n\t@OneToMany(mappedBy = "category" , cascade = CascadeType.ALL, fetch = FetchType.LAZY)\\n\tprivate List<Post> posts = new ArrayList<>(); \\n\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\entity\\Post.java',
                    'fileContent': 'package com.suraj.blog.entity;\\n\\nimport java.util.Date;\\nimport java.util.HashSet;\\nimport java.util.Set;\\n\\nimport javax.persistence.CascadeType;\\nimport javax.persistence.Column;\\nimport javax.persistence.Entity;\\nimport javax.persistence.GeneratedValue;\\nimport javax.persistence.GenerationType;\\nimport javax.persistence.Id;\\nimport javax.persistence.JoinColumn;\\nimport javax.persistence.ManyToOne;\\nimport javax.persistence.OneToMany;\\n\\nimport lombok.Getter;\\nimport lombok.NoArgsConstructor;\\nimport lombok.Setter;\\n\\n@Entity\\n@Getter\\n@Setter\\n@NoArgsConstructor\\npublic class Post {\\n\\n\t@Id\\n\t@GeneratedValue(strategy = GenerationType.IDENTITY)\\n\tprivate Integer postId;\\n\t@Column(name="post_title", nullable = false, length = 100)\\n\tprivate String title;\\n\t\\n\t@Column(length = 10000)\\n\tprivate String content;\\n\t\\n\tprivate String imageName;\\n\tprivate Date addedDate;\\n\\n\t@ManyToOne\\n\t@JoinColumn(name = "categoryId")\\n\tprivate Category category;\\n\\n\t@ManyToOne\\n\tprivate User user;\\n\t\\n\t@OneToMany(mappedBy = "post", cascade = CascadeType.ALL)\\n\tprivate Set<Comment> comments = new HashSet<Comment>();\\n\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\entity\\User.java',
                    'fileContent': 'package com.suraj.blog.entity;\\n\\nimport java.util.ArrayList;\\nimport java.util.List;\\n\\nimport javax.persistence.CascadeType;\\nimport javax.persistence.Column;\\nimport javax.persistence.Entity;\\nimport javax.persistence.FetchType;\\nimport javax.persistence.GeneratedValue;\\nimport javax.persistence.GenerationType;\\nimport javax.persistence.Id;\\nimport javax.persistence.OneToMany;\\nimport javax.persistence.Table;\\n\\n\\nimport lombok.Getter;\\nimport lombok.NoArgsConstructor;\\nimport lombok.Setter;\\n\\n@Entity\\n@Table(name = "users")\\n@Getter\\n@Setter\\n@NoArgsConstructor\\npublic class User {\\n\\n\t@Id\\n\t@GeneratedValue(strategy = GenerationType.AUTO)\\n\tprivate int id;\\n\t@Column(nullable = false, length =100)\\n\tprivate String name;\\n\tprivate String email;\\n\tprivate String password;\\n\tprivate String about;\\n\t\\n\t@OneToMany(mappedBy = "user" , cascade = CascadeType.ALL, fetch = FetchType.LAZY)\\n\tprivate List<Post> posts = new ArrayList<>(); \\n\t\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\payload\\PostDto.java',
                    'fileContent': 'package com.suraj.blog.payload;\\n\\nimport java.util.HashSet;\\nimport java.util.Set;\\n\\nimport com.suraj.blog.entity.Comment;\\n\\nimport lombok.Getter;\\nimport lombok.NoArgsConstructor;\\nimport lombok.Setter;\\n\\n@Getter\\n@Setter\\n@NoArgsConstructor\\npublic class PostDto {\\n\\n\tprivate Integer postId;\\n\tprivate String title;\\n\tprivate String content;\\n\tprivate String imageName;\\n\tprivate String addedDate;\\n\tprivate CategoryDTO category;\\n\tprivate UserDTO user;\\n\tprivate Set<CommentDto> comments=new HashSet<>();\\n\\n}\\n'
                },
                {
                    'filePath': 'e:\\Graduation Project\\Projects\\Dataset\\BlogBackend-main\\blog-api-com\\src\\main\\java\\com\\suraj\\blog\\service\\impl\\x.java',
                    'fileContent': 'package com.suraj.blog.service.impl;\r\\n\r\\nimport java.util.Date;\r\\nimport java.util.List;\r\\nimport java.util.stream.Collectors;\r\\n\r\\nimport org.modelmapper.ModelMapper;\r\\nimport org.springframework.beans.factory.annotation.Autowired;\r\\nimport org.springframework.data.domain.Page;\r\\nimport org.springframework.data.domain.PageRequest;\r\\nimport org.springframework.data.domain.Pageable;\r\\nimport org.springframework.data.domain.Sort;\r\\nimport org.springframework.stereotype.Service;\r\\n\r\\nimport com.suraj.blog.dao.CategoryRepo;\r\\nimport com.suraj.blog.dao.PostRepo;\r\\nimport com.suraj.blog.dao.UserRepo;\r\\nimport com.suraj.blog.entity.Category;\r\\nimport com.suraj.blog.entity.Post;\r\\nimport com.suraj.blog.entity.User;\r\\nimport com.suraj.blog.exceptions.ResourceNotFoundException;\r\\nimport com.suraj.blog.payload.PostDto;\r\\nimport com.suraj.blog.service.PostService;\r\\nimport com.suraj.blog.service.PostMapper;\r\\n\r\\n@Service\r\\npublic class PostServiceImpl implements PostService {\r\\n\r\\n    @Autowired\r\\n    private PostRepo postRepo;\r\\n\r\\n    @Autowired\r\\n    private UserRepo userRepo;\r\\n\r\\n    @Autowired\r\\n    private CategoryRepo categoryRepo;\r\\n\r\\n    @Autowired\r\\n    private PostMapper postMapper;\r\\n\r\\n    @Override\r\\n    public PostDto createPost(PostDto postDto, Integer userId, Integer categoryId) {\r\\n        User user = this.userRepo.findById(userId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("User", "userId", userId));\r\\n        Category category = this.categoryRepo.findById(categoryId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("Category", "categoryId", categoryId));\r\\n        Post post = postMapper.toEntity(postDto);\r\\n        post.setImageName("default.png");\r\\n        post.setAddedDate(new Date());\r\\n        post.setUser(user);\r\\n        post.setCategory(category);\r\\n        Post newPost = this.postRepo.save(post);\r\\n        return postMapper.toDto(newPost);\r\\n    }\r\\n\r\\n    @Override\r\\n    public PostDto updatePost(PostDto postDto, Integer postId) {\r\\n        Post post = this.postRepo.findById(postId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));\r\\n        postMapper.update(post, postDto);\r\\n        Post updatedPost = this.postRepo.save(post);\r\\n        return postMapper.toDto(updatedPost);\r\\n    }\r\\n\r\\n    @Override\r\\n    public void deletePost(Integer postId) {\r\\n        Post post = this.postRepo.findById(postId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));\r\\n        this.postRepo.delete(post);\r\\n    }\r\\n\r\\n    @Override\r\\n    public List<PostDto> getAllPost(Integer pageNumber, Integer pageSize, String sortBy, String sortDir) {\r\\n        Sort sort = Sort.by(sortBy);\r\\n        if (sortDir.equalsIgnoreCase("a")) {\r\\n            sort = sort.ascending();\r\\n        } else {\r\\n            sort = sort.descending();\r\\n        }\r\\n        Pageable p = PageRequest.of(pageNumber, pageSize, sort);\r\\n        Page<Post> page = this.postRepo.findAll(p);\r\\n        List<Post> posts = page.getContent();\r\\n        return posts.stream().map(postMapper::toDto).collect(Collectors.toList());\r\\n    }\r\\n\r\\n    @Override\r\\n    public PostDto getPostById(Integer postId) {\r\\n        Post post = this.postRepo.findById(postId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("Post", "post id", postId));\r\\n        return postMapper.toDto(post);\r\\n    }\r\\n\r\\n    @Override\r\\n    public List<PostDto> getPostByCategory(Integer categoryId) {\r\\n        Category category = this.categoryRepo.findById(categoryId)\r\\n                .orElseThrow(() -> new ResourceNotFoundException("Category", "categoryId", categoryId));\r\\n        List<Post> posts = this.postRepo.findByCategory(category);\r\\n        return posts.stream().map(postMapper::toDto).collect(Collectors.toList());\r\\n    }\r\\n\r\\n    @Override\r\\n    public List<PostDto> getPostByUser(Integer userId) {\r\\n        User user = this.userRepo.findById(userId)\r\\n.orElseThrow(() -> new ResourceNotFoundException("User", "userId", userId));\r\\nList < Post > posts = this.postRepo.findByUser(user);\r\\n return posts.stream().map(postMapper::toDto).collect(Collectors.toList());\r\\n}\r\\n\r\\n @ Override\r\\n public List < PostDto > searchPosts(String Keyword) {\r\\nList < Post > posts = this.postRepo.findByTitleContaining(Keyword);\r\\n return posts.stream().map(postMapper::toDto).collect(Collectors.toList());\r\\n}\r\\n}\r\\n'
                }
            ]
        }
    except Exception as e:
        print(f"Error processing file {files.data[0].mainFilePath}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing {files.data[0].mainFilePath}: {str(e)}"
        )



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