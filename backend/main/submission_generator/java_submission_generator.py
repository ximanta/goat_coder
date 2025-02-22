from typing import Dict, Any
import re
import logging
import json
import os
from ..utils.name_converter import to_java_name

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
            
            # Log the function name conversion
            logger.info(f"Checking for function name: {java_function_name} (original: {python_function_name})")
            logger.info(f"Function name: {java_function_name}")

            # Extract input and output structure
            input_structure = problem_structure.get("input_structure", [])
            output_structure = problem_structure.get("output_structure", {})
            
            logger.info(f"Input structure: {input_structure}")
            logger.info(f"Output structure: {output_structure}")

            # Generate parameter list for function signature
            param_list = []
            for param in input_structure:
                param_type = param["Input_Field"].split()[0]
                param_name = param["Input_Field"].split()[1]
                java_type = self._convert_type_to_java(param_type)
                java_param_name = to_java_name(param_name)
                param_list.append(f"{java_type} {java_param_name}")

            logger.info(f"Parameter list: {param_list}")

            # Get return type
            return_type = output_structure["Output_Field"].split()[0]
            return_type = self._convert_type_to_java(return_type)
            logger.info(f"Return type: {return_type}")

            # Extract the function body from the source code
            code_body = source_code

            # Generate input parsing code
            input_parsing_code = []
            total_inputs = len(input_structure)
            for i, param in enumerate(input_structure):
                param_type = param["Input_Field"].split()[0]
                param_name = param["Input_Field"].split()[1]
                java_type = self._convert_type_to_java(param_type)
                java_param_name = to_java_name(param_name)
                input_parsing_code.append(
                    self._generate_input_parsing(java_type, java_param_name, i, total_inputs)
                )

            # Join all the parts together
            function_params = ", ".join(param_list)
            function_call_args = ", ".join(to_java_name(p["Input_Field"].split()[1]) for p in input_structure)
            class_name = "Main"

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
                function_name=java_function_name,
                function_params=function_params,
                source_code=code_body.strip(),
                input_parsing_code="\n        ".join(input_parsing_code),
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
            raise JavaSubmissionGeneratorException(f"Failed to generate Java submission: {str(e)}")

    def _validate_problem_structure(self, problem_structure: Dict[str, Any]):
        """
        Validates that the problem structure contains all required fields.
        """
        required_fields = ["problem_name", "function_name", "input_structure", "output_structure"]
        for field in required_fields:
            if field not in problem_structure:
                raise JavaSubmissionGeneratorException(f"Missing required field: {field}")

    def _validate_source_code(self, source_code: str, problem_structure: Dict[str, Any]):
        """
        Validates that the source code contains the expected function name.
        Converts the Python-style function name to Java convention before checking.
        """
        if not source_code or not source_code.strip():
            raise JavaSubmissionGeneratorException("Source code is empty")

        # Convert Python function name to Java convention
        python_function_name = problem_structure.get("function_name")
        if not python_function_name:
            raise JavaSubmissionGeneratorException("Function name not found in problem structure")

        java_function_name = to_java_name(python_function_name)
        if java_function_name not in source_code:
            raise JavaSubmissionGeneratorException(
                f"Source code does not contain the expected function: {java_function_name}"
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
            raise JavaSubmissionGeneratorException("Map types not supported for input parsing yet")

        # Handle array types
        if java_type.endswith("[]"):
            base_type = java_type[:-2]
            return self._parse_array_input(base_type, param_name)

        # Handle primitive and String types
        return f"{java_type} {param_name} = {self._parse_value(java_type, param_name)};"

    def _parse_array_input(self, base_type: str, var_name: str) -> str:
        """Helper method to parse array input"""
        parse_method = {
            "int": "Integer.parseInt",
            "double": "Double.parseDouble",
            "boolean": "Boolean.parseBoolean",
            "long": "Long.parseLong",
            "float": "Float.parseFloat",
            "byte": "Byte.parseByte",
            "short": "Short.parseShort"
        }.get(base_type, "")

        if base_type == "String":
            return f"""String[] {var_name} = scanner.nextLine().split(" ");"""
        elif parse_method:
            return f"""String[] {var_name}Str = scanner.nextLine().split(" ");
        {base_type}[] {var_name} = new {base_type}[{var_name}Str.length];
        for (int i = 0; i < {var_name}Str.length; i++) {{
            {var_name}[i] = {parse_method}({var_name}Str[i]);
        }}"""
        else:
            raise JavaSubmissionGeneratorException(f"Unsupported array base type: {base_type}")

    def _parse_value(self, java_type: str, var_name: str) -> str:
        """Helper method to generate parsing code for different types"""
        type_to_parse = {
            "int": "Integer.parseInt(scanner.nextLine())",
            "double": "Double.parseDouble(scanner.nextLine())",
            "boolean": "Boolean.parseBoolean(scanner.nextLine())",
            "String": "scanner.nextLine()",
            "long": "Long.parseLong(scanner.nextLine())",
            "float": "Float.parseFloat(scanner.nextLine())",
            "byte": "Byte.parseByte(scanner.nextLine())",
            "short": "Short.parseShort(scanner.nextLine())",
            "char": "scanner.nextLine().charAt(0)"
        }
        return type_to_parse.get(java_type, "scanner.nextLine()")

    def _generate_output_printing(self, return_type: str, var_name: str) -> str:
        """
        Generates Java code to print the output based on its type.
        Just prints the array contents directly without Python-style formatting.
        """
        if return_type.endswith("[]"):
            return f"""if ({var_name} == null) {{
            System.out.println("null");
        }} else {{
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < {var_name}.length; i++) {{
                if (i > 0) sb.append(" ");
                sb.append({var_name}[i]);
            }}
            System.out.println(sb.toString());
        }}"""
        else:
            return f"System.out.println({var_name});"
