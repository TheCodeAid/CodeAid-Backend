from fastapi import HTTPException
from models import CouplingViolationFix, RefactoringRequestData, couplingSuggestionIn



class RefactoringManager:
    def __init__(self, solid_handler, coupling_handler, response_manager):
        self.solid_handler = solid_handler
        self.coupling_handler = coupling_handler
        self.response_manager = response_manager

    def refactor_solid(self, files: RefactoringRequestData):
        refactoredCode = []
        try:
            refactored_files = self.solid_handler.refactorMainFile(files)
            print(refactored_files)
            if refactored_files is None:
                print(f"Warning: refactor returned None for file {files.data[0].mainFilePath}")
            else:
                mainfile_extracted_response = self.response_manager.extract_response(refactored_files)
                try:
                    self.response_manager.validate_response(mainfile_extracted_response)
                except:
                    print("Failed to validate refactored main file")
                for item in mainfile_extracted_response:
                    cleanedContent = self.response_manager.cleanContent(item.get("fileContent"))
                    refactoredCode.append({
                        "filePath": item.get("filePath"),
                        "fileContent": cleanedContent
                    })
                for entry in files.data:
                    dependents = entry.dependents
                    dependency_result = self.solid_handler.refactorDependencyFiles(
                        files.data[0].mainFileContent,
                        dependents,
                        mainfile_extracted_response
                    )
                    extracted_response = self.response_manager.extract_response(dependency_result)
                    try:
                        self.response_manager.validate_response(extracted_response)
                    except:
                        print("Failed to validate refactored dependency file")
                    for item in extracted_response:
                        refactoredCode.append(item)

            return {
                "refactored_files": refactoredCode
            }
            # return {
            # "refactored_files": [{'filePath': 'c:\\Users\\Mariam\\OneDrive\\Documents\\GitHub\\Toffee\\OrderService.java', 'fileContent': 'import java.io.IOException; public class OrderService { public void saveOrder(Order order) throws IOException { if (order != null) { boolean idSet = false; while (!idSet) { Random random = new Random(); int orderId = random.nextInt(100, 999); try { BufferedReader reader1 = new BufferedReader(new FileReader(\"NDeliveredOrders.csv\")); String line1; while ((line1 = reader1.readLine()) != null) { String[] values = line1.split(\\",\\"); if (Integer.toString(order.getID()).equals(values[0])) { break; } } reader1.close(); BufferedReader reader2 = new BufferedReader(new FileReader(\\"DeliveredOrders.csv\\")); String line2; while ((line2 = reader2.readLine()) != null) { String[] values = line2.split(\\",\\"); if (Integer.toString(order.getID()).equals(values[0])) { break; } } reader2.close(); idSet = true; order.setID(orderId); } catch (IOException e) { System.out.println(\\"An error occurred while reading the CSV file: \\" + e.getMessage()); e.printStackTrace(); } } String line = order.getID() + \\",\\" + order.getDDate() + \\",\\" + order.getPMethod() + \\",\\" + order.getTotalPrice(); OrderFileWriter orderFileWriter = new OrderFileWriter(); orderFileWriter.writeOrder(line); System.out.println(\\"Your Order is Placed Successfully With ID \\" + order.getID() + \' \'); } public void removeOrder(String Date) throws IOException { OrderFileRemover orderFileRemover = new OrderFileRemover(); orderFileRemover.removeOrder(Date); } }'}] 
            #         }
        except Exception as e:
            print(f"Error processing file {files.data[0].mainFilePath}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {files.data[0].mainFilePath}: {str(e)}"
            )

    def refactor_coupling(self, file: couplingSuggestionIn):
        print("Received files for refactoring:", file)
        results = []
        suggestions = []
        try:
            suggestions = self.coupling_handler.refactor(file)
            if suggestions is None:
                print(f"Warning: refactor returned None for file {file.coupling_smells[0].files[0].filePath}")
            else:
                suggestions = self.response_manager.extract_response(suggestions)
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
