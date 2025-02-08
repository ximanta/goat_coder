from typing import Dict, Any
import re
from main.submission_generator.java_submission_generator import JavaSubmissionGenerator, JavaSubmissionGeneratorException

class JavaSubmissionGeneratorException(Exception):
    pass

class JavaSubmissionGenerator:
    def generate_submission(self, source_code: str, problem_structure: Dict[str, Any]) -> str:
        """
        Generates a complete Java submission by combining the source code with the problem structure.
        
        Args:
            source_code (str): The user's source code implementation
            problem_structure (Dict[str, Any]): The problem structure containing function and input/output details
            
        Returns:
            str: Complete Java code ready for compilation and execution
            
        Raises:
            JavaSubmissionGeneratorException: If validation fails
        """
        # Validate problem structure
        self._validate_problem_structure(problem_structure)
        
        # Validate source code
        self._validate_source_code(source_code, problem_structure)
        
        function_name = problem_structure.get("function_name")
        input_structure = problem_structure.get("input_structure")
        output_structure = problem_structure.get("output_structure")
        
        # Create the class wrapper
        class_name = "Solution"
        
        # Generate the method signature based on input/output structure
        param_list = []
        param_parsing = []
        for i, input_field in enumerate(input_structure):
            field = input_field["Input_Field"].split()
            java_type = self._convert_type_to_java(field[0])
            param_name = field[1]
            param_list.append(f"{java_type} {param_name}")
            param_parsing.append(self._generate_input_parsing(java_type, param_name, i))
            
        # Get return type
        output_field = output_structure["Output_Field"].split()
        return_type = self._convert_type_to_java(output_field[0])
        
        # Precompute the joined strings to avoid backslashes in f-string expressions
        input_parsing_code = "\n        ".join(param_parsing)
        # Extract the parameter names (assumes each param in param_list is like "int a")
        function_call_args = ", ".join(p.split()[-1] for p in param_list)
        
        # Combine everything into the final submission with required imports
        submission = f"""import java.util.*;

public class {class_name} {{
    public {return_type} {function_name}({', '.join(param_list)}) {{
        {source_code}
    }}

    public static void main(String[] args) {{
        Scanner scanner = new Scanner(System.in);
        Solution solution = new Solution();
        
        // Parse input
        {input_parsing_code}
        
        // Call the solution function
        {return_type} result = solution.{function_name}({function_call_args});
        
        // Print the result
        {self._generate_output_printing(return_type, 'result')}
        
        scanner.close();
    }}
}}
"""
        return submission.strip()

    def _validate_problem_structure(self, problem_structure: Dict[str, Any]) -> None:
        """
        Validates that the problem structure contains all required fields.
        """
        required_fields = ["function_name", "input_structure", "output_structure"]
        for field in required_fields:
            if field not in problem_structure:
                raise JavaSubmissionGeneratorException(f"Missing required field: {field}")
        
        if not isinstance(problem_structure["input_structure"], list):
            raise JavaSubmissionGeneratorException("input_structure must be a list")
        
        if not isinstance(problem_structure["output_structure"], dict):
            raise JavaSubmissionGeneratorException("output_structure must be a dictionary")
            
        if "Output_Field" not in problem_structure["output_structure"]:
            raise JavaSubmissionGeneratorException("output_structure must contain Output_Field")

    def _validate_source_code(self, source_code: str, problem_structure: Dict[str, Any]) -> None:
        """
        Validates the source code for basic Java syntax and return statement presence.
        """
        if not source_code.strip():
            raise JavaSubmissionGeneratorException("Source code cannot be empty")
        
        # Check for return statement presence
        if "return" not in source_code:
            raise JavaSubmissionGeneratorException("Source code must contain a return statement")
        
        # Basic Java syntax validation
        try:
            # Check for unmatched braces
            open_braces = source_code.count("{")
            close_braces = source_code.count("}")
            if open_braces != close_braces:
                raise JavaSubmissionGeneratorException("Unmatched braces in source code")
            
            # Check for semicolon at end of statements
            lines = [line.strip() for line in source_code.split("\n") if line.strip()]
            for line in lines:
                if (line.endswith(("{", "}")) or line.startswith("//") 
                    or "for" in line or "if" in line or "while" in line):
                    continue
                if not line.endswith(";"):
                    raise JavaSubmissionGeneratorException("Missing semicolon in statement")
                    
        except Exception as e:
            raise JavaSubmissionGeneratorException(f"Invalid Java syntax: {str(e)}")
    
    def _convert_type_to_java(self, python_type: str) -> str:
        """
        Converts Python type hints to Java type declarations.
        
        Args:
            python_type (str): Python type hint (e.g., 'List[int]', 'str', 'int')
            
        Returns:
            str: Corresponding Java type
        """
        type_mapping = {
            "str": "String",
            "int": "int",
            "float": "double",
            "bool": "boolean",
            "List[int]": "int[]",
            "List[str]": "String[]",
            "List[float]": "double[]",
            "List[bool]": "boolean[]"
        }
        return type_mapping.get(python_type, "Object")

    def _generate_input_parsing(self, java_type: str, param_name: str, index: int) -> str:
        """Generate code to parse input based on type"""
        if java_type == "int[]":
            return f"""String[] input{index} = scanner.nextLine().split(" ");
            int[] {param_name} = new int[input{index}.length];
            for(int i = 0; i < input{index}.length; i++) {{
                {param_name}[i] = Integer.parseInt(input{index}[i]);
            }}"""
        elif java_type == "String[]":
            return f"{param_name} = scanner.nextLine().split(\" \");"
        elif java_type == "int":
            return f"{param_name} = Integer.parseInt(scanner.nextLine());"
        elif java_type == "String":
            return f"{param_name} = scanner.nextLine();"
        return f"{param_name} = scanner.nextLine();"

    def _generate_output_printing(self, return_type: str, var_name: str) -> str:
        """Generate code to print output based on type"""
        if return_type.endswith("[]"):
            return f"System.out.println(Arrays.toString({var_name}));"
        return f"System.out.println({var_name});"

def main():
    # Example source code and problem structure for testing
    source_code = """
       public int[] increment_array(int[] array, int incrementValue) {
    // Create a new array to store the incremented values
    int[] incrementedArray = new int[array.length];
    
    // Loop through each element and add the incrementValue
    for (int i = 0; i < array.length; i++) {
        incrementedArray[i] = array[i] + incrementValue;
    }
    
    // Return the updated array
    return incrementedArray;
}
    """
    
    problem_structure = {
      "problem_name": "Array Increment Operation",
    "function_name": "increment_array",
    "input_structure": [
      {
        "Input_Field": "List[int] array"
      },
      {
        "Input_Field": "int incrementValue"
      }
    ],
    "output_structure": {
      "Output_Field": "List[int] incrementedArray"
    }
    }
    
    generator = JavaSubmissionGenerator()
    try:
        generated_submission = generator.generate_submission(source_code, problem_structure)
        print("Generated Java Submission:\n")
        print(generated_submission)
        
        # Save to a file for testing
        with open("Solution.java", "w") as f:
            f.write(generated_submission)
        print("\nSaved to Solution.java")
        
    except JavaSubmissionGeneratorException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
