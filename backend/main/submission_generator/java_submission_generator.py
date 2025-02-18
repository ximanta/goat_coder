from typing import Dict, Any
import re
import logging
import json
import os
from ..utils.name_converter import to_java_name  # Fix duplicate import line

# Set up logging
logger = logging.getLogger(__name__)

class JavaSubmissionGeneratorException(Exception):
    """Custom exception for errors during Java submission generation."""
    pass

class JavaSubmissionGenerator:
    def __init__(self):
        # Add a debug directory for saving generated files
        self.debug_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'debug')
        os.makedirs(self.debug_dir, exist_ok=True)

    def generate_submission(self, source_code: str, problem_structure: Dict[str, Any]) -> str:
        """
        Generates a complete Java submission by combining the user's source code
        with the problem structure details (function name, input/output details).

        Args:
            source_code (str): The user's source code implementation.
            problem_structure (Dict[str, Any]): Contains function and input/output details.

        Returns:
            str: Complete Java code ready for compilation and execution.

        Raises:
            JavaSubmissionGeneratorException: If validation fails.
        """
        try:
            # Log incoming data for debugging.
            logger.info("Generating Java submission:")
            logger.info(f"Source code: {source_code}")
            logger.info(f"Problem structure: {problem_structure}")
            
            # Validate the structure of the problem JSON.
            self._validate_problem_structure(problem_structure)
            
            # Validate that the source code contains the expected function.
            self._validate_source_code(source_code, problem_structure)
            
            # Convert the Python function name to Java's naming convention.
            python_function_name = problem_structure.get("function_name")
            java_function_name = to_java_name(python_function_name)
            
            # Update the problem structure to use the Java-style function name.
            java_problem_structure = {
                **problem_structure,
                "function_name": java_function_name
            }
            
            function_name = java_problem_structure.get("function_name")
            input_structure = java_problem_structure.get("input_structure")
            output_structure = java_problem_structure.get("output_structure")
            
            # Log parsed components.
            logger.info(f"Function name: {function_name}")
            logger.info(f"Input structure: {input_structure}")
            logger.info(f"Output structure: {output_structure}")
            
            # Define the class name for the generated Java code.
            class_name = "Main"
            
            # Generate the method signature and input parsing code.
            param_list = []
            param_parsing = []
            num_inputs = len(input_structure)
            for i, input_field in enumerate(input_structure):
                # Each input field is specified as "Type variableName".
                field = input_field["Input_Field"].split()
                java_type = self._convert_type_to_java(field[0])
                param_name = to_java_name(field[1])
                param_list.append(f"{java_type} {param_name}")
                # Generate input parsing code for this parameter.
                param_parsing.append(self._generate_input_parsing(java_type, param_name, i, num_inputs))
                
            # Determine the return type from the output structure.
            output_field = output_structure["Output_Field"].split()
            return_type = self._convert_type_to_java(output_field[0])
            
            # Log the generated method parameters and return type.
            logger.info(f"Parameter list: {param_list}")
            logger.info(f"Return type: {return_type}")
            
            # Join the generated input parsing code lines.
            input_parsing_code = "\n        ".join(param_parsing)
            function_params = ", ".join(param_list)
            function_call_args = ", ".join([p.split()[-1] for p in param_list])
            
            # Remove any existing class or method wrappers from the user's source code.
            # code_body = re.sub(r'public.*?\{', '', source_code)
            # code_body = re.sub(r'\}[\s]*$', '', code_body)
            code_body=source_code
            # Create the final submission template.
            submission_template = """import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class {class_name} {{

{source_code}


    public static void main(String[] args) {{
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        {input_parsing_code}
        
        // Call the solution function
        {return_type} result = solution.{function_name}({function_call_args});
        
        // Print the result
        {output_printing}
        scanner.close();
    }}
}}"""

            submission = submission_template.format(
                class_name=class_name,
                return_type=return_type,
                function_name=function_name,
                function_params=function_params,
                source_code=code_body.strip(),
                input_parsing_code=input_parsing_code,
                function_call_args=function_call_args,
                output_printing=self._generate_output_printing(return_type, 'result')
            )
            
            # Save the generated code to a file for debugging with full path
            debug_file_path = os.path.join(self.debug_dir, 'Main.java')
            try:
                with open(debug_file_path, 'w', encoding='utf-8') as f:
                    f.write(submission.strip())
                logger.info(f"Successfully saved generated Java code to {debug_file_path}")
                # Also log the content being written
                logger.info("Content being written to file:")
                logger.info(submission.strip())
            except Exception as e:
                logger.error(f"Failed to save {debug_file_path}: {str(e)}")
            
            logger.info("=== Generated Java Submission ===")
            logger.info(f"Generated submission:\n{submission}")
            return submission.strip()
        except Exception as e:
            logger.error(f"Error generating Java submission: {str(e)}")
            raise

    def _validate_problem_structure(self, problem_structure: Dict[str, Any]) -> None:
        """
        Validates that the problem structure contains all required fields.
        """
        required_fields = ["function_name", "input_structure", "output_structure"]
        for field in required_fields:
            if (field not in problem_structure):
                raise JavaSubmissionGeneratorException(f"Missing required field: {field}")
        
        if not isinstance(problem_structure["input_structure"], list):
            raise JavaSubmissionGeneratorException("input_structure must be a list")
        
        if not isinstance(problem_structure["output_structure"], dict):
            raise JavaSubmissionGeneratorException("output_structure must be a dictionary")
        
        if "Output_Field" not in problem_structure["output_structure"]:
            raise JavaSubmissionGeneratorException("output_structure must contain Output_Field")

    def _validate_source_code(self, source_code: str, problem_structure: Dict[str, Any]) -> None:
        """
        Validates that the source code contains the expected function name.
        Converts the Python-style function name to Java convention before checking.
        """
        # Remove comments and extraneous whitespace.
        code = re.sub(r'//.*?\n|/\*.*?\*/', '', source_code, flags=re.S)
        code = code.strip()

        function_name = problem_structure.get("function_name")
        if not function_name:
            raise JavaSubmissionGeneratorException("Missing function name in problem structure")

        # Convert Python snake_case to Java camelCase.
        java_function_name = to_java_name(function_name)
        
        logger.info(f"Checking for function name: {java_function_name} (original: {function_name})")

        # Check if the Java-style function name exists in the code.
        if java_function_name not in code:
            raise JavaSubmissionGeneratorException(
                f"Function '{java_function_name}' not found in source code"
            )

    def _convert_type_to_java(self, python_type: str) -> str:
        """
        Converts Python type hints to Java type declarations.
        """
        python_type = python_type.lower()
        
        # Handle dictionary/map types
        if python_type.startswith("dict[") or python_type.startswith("map["):
            # Extract key and value types from dict[str, list[int]] format
            inner_types = python_type[python_type.find("[")+1:python_type.rfind("]")]
            key_type, value_type = [t.strip() for t in inner_types.split(",", 1)]
            
            # Convert the key and value types
            java_key_type = self._convert_type_to_java(key_type)
            java_value_type = self._convert_type_to_java(value_type)
            
            return f"Map<{java_key_type}, {java_value_type}>"

        # Handle list types - now converting to arrays
        if python_type.startswith("list["):
            inner_type = python_type[5:-1]  # Extract type inside List[]
            if inner_type == "int":
                return "int[]"
            elif inner_type in ("str", "string"):
                return "String[]"
            elif inner_type == "float":
                return "double[]"
            elif inner_type == "bool":
                return "boolean[]"
            else:
                # Try to convert the inner type recursively
                java_inner_type = self._convert_type_to_java(inner_type)
                return f"{java_inner_type}[]"

        # Mapping for simple types
        type_mapping = {
            "str": "String",
            "string": "String",
            "int": "int",        # Changed back to primitive
            "float": "double",   # Changed back to primitive
            "bool": "boolean",   # Changed back to primitive
            "object": "Object"
        }
        
        return type_mapping.get(python_type, "Object")

    def _generate_input_parsing(self, java_type: str, param_name: str, index: int, total_inputs: int) -> str:
        """
        Generates Java code that parses input from the Scanner based on the type.
        """
        # Handle Map types
        if java_type.startswith("Map<"):
            return (
                f"Map{java_type[3:]} {param_name} = new HashMap<>();\n"
                f"        while (scanner.hasNextLine()) {{\n"
                f"            String line = scanner.nextLine().trim();\n"
                f"            if (line.isEmpty()) break;\n"
                f"            String[] parts = line.split(\":\", 2);\n"
                f"            if (parts.length == 2) {{\n"
                f"                String key = parts[0].trim();\n"
                f"                String[] values = parts[1].trim().split(\"\\\\s+\");\n"
                f"                List<Integer> scores = new ArrayList<>();\n"
                f"                for (String val : values) {{\n"
                f"                    scores.add(Integer.parseInt(val));\n"
                f"                }}\n"
                f"                {param_name}.put(key, scores);\n"
                f"            }}\n"
                f"        }}"
            )

        # Handle array types
        if java_type.endswith("[]"):
            base_type = java_type[:-2]
            parse_method = ""
            if base_type == "int":
                parse_method = "Integer.parseInt"
            elif base_type == "double":
                parse_method = "Double.parseDouble"
            elif base_type == "boolean":
                parse_method = "Boolean.parseBoolean"
            else:
                parse_method = ""  # String doesn't need parsing
                
            return (
                f"String line = scanner.hasNextLine() ? scanner.nextLine().trim() : \"\";\n"
                f"        {java_type} {param_name};\n"
                f"        if (line.isEmpty()) {{\n"
                f"            {param_name} = new {base_type}[0];\n"
                f"        }} else {{\n"
                f"            String[] allItems = line.split(\"\\\\s+\");\n"
                f"            {param_name} = new {base_type}[allItems.length];\n"
                f"            for (int i = 0; i < allItems.length; i++) {{\n"
                f"                {param_name}[i] = {parse_method}(allItems[i].trim());\n"
                f"            }}\n"
                f"        }}"
            )

        # Handle simple types
        type_parsing = {
            "String": f"String {param_name} = scanner.nextLine();",
            "int": f"int {param_name} = Integer.parseInt(scanner.nextLine());",
            "double": f"double {param_name} = Double.parseDouble(scanner.nextLine());",
            "boolean": f"boolean {param_name} = Boolean.parseBoolean(scanner.nextLine());",
        }
        
        return type_parsing.get(java_type, f"String {param_name} = scanner.nextLine();")

    def _parse_value(self, java_type: str, var_name: str) -> str:
        """Helper method to generate parsing code for different types"""
        type_parsing = {
            "Integer": f"Integer.parseInt({var_name})",
            "Double": f"Double.parseDouble({var_name})",
            "Boolean": f"Boolean.parseBoolean({var_name})",
            "String": var_name
        }
        return type_parsing.get(java_type, var_name)

    def _generate_output_printing(self, return_type: str, var_name: str) -> str:
        """
        Generates Java code to print the output based on its type.
        Just prints the array contents directly without Python-style formatting.
        """
        if (return_type.endswith("[]")):
            return f"System.out.println(Arrays.toString({var_name}));"
        return f"System.out.println({var_name});"

    def format_input(self, input_data: list) -> str:
        """
        Format input data for Java program stdin.
        - For array inputs: elements should be space-separated on one line
        - For multiple separate inputs: each parameter on a new line
        """
        formatted_inputs = []
        for item in input_data:
            if isinstance(item, list):
                # Array elements stay space-separated on one line
                formatted_items = [str(x) for x in item]
                formatted_inputs.append(" ".join(formatted_items))
            elif len(input_data) > 1:
                # Multiple scalar parameters each get their own line
                formatted_inputs.append(str(item))
            else:
                # Single scalar parameter
                formatted_inputs.append(str(item))
        
        return "\n".join(formatted_inputs)

#     def _generate_submission_template(self, class_name: str, return_type: str, 
#                                         function_name: str, param_list: list, 
#                                         source_code: str, param_parsing: list) -> str:
#         """
#         (Unused in this implementation) Generates the complete Java submission template.
#         """
#         # Join the parameters and input parsing code.
#         function_params = ", ".join(param_list)
#         input_parsing_code = "\n        ".join(param_parsing)
#         function_call_args = ", ".join(p.split()[-1] for p in param_list)
        
#         template = f"""import java.util.*;
# import java.util.regex.*;
# public class {class_name} {{
#     public {return_type} {function_name}({function_params}) {{
#         {source_code}
#     }}
#     public static void main(String[] args) {{
#         Scanner scanner = new Scanner(System.in);
#         Solution solution = new Solution();
        
#         // Parse input
#         {input_parsing_code}
        
#         // Call the solution function
#         {return_type} result = solution.{function_name}({function_call_args});
        
#         // Print the result
#         System.out.println(result);
        
#         scanner.close();
#     }}
# }}"""
#         console.log("java_submission_generator: Submission template geerated:", template)
#         return template
