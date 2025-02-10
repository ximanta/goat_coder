from typing import Dict, Any
import re
import logging
from ..utils.name_converter import to_java_name

logger = logging.getLogger(__name__)

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
        try:
            # Log incoming data
            logger.info("Generating Java submission:")
            logger.info(f"Source code: {source_code}")
            logger.info(f"Problem structure: {problem_structure}")
            
            # Validate problem structure
            self._validate_problem_structure(problem_structure)
            
            # Validate source code
            self._validate_source_code(source_code, problem_structure)
            
            # Convert function name to Java convention
            python_function_name = problem_structure.get("function_name")
            java_function_name = to_java_name(python_function_name)
            
            # Create a copy of the problem structure with the Java-style function name
            java_problem_structure = {
                **problem_structure,
                "function_name": java_function_name
            }
            
            function_name = java_problem_structure.get("function_name")
            input_structure = java_problem_structure.get("input_structure")
            output_structure = java_problem_structure.get("output_structure")
            
            # Log parsed components
            logger.info(f"Function name: {function_name}")
            logger.info(f"Input structure: {input_structure}")
            logger.info(f"Output structure: {output_structure}")
            
            # Create the class wrapper
            class_name = "Main"
            
            # Generate the method signature based on input/output structure
            param_list = []
            param_parsing = []
            num_inputs = len(input_structure)
            for i, input_field in enumerate(input_structure):
                field = input_field["Input_Field"].split()
                java_type = self._convert_type_to_java(field[0])
                param_name = to_java_name(field[1])
                param_list.append(f"{java_type} {param_name}")
                param_parsing.append(self._generate_input_parsing(java_type, param_name, i, num_inputs))
                
            # Get return type
            output_field = output_structure["Output_Field"].split()
            return_type = self._convert_type_to_java(output_field[0])
            
            # Log generated components
            logger.info(f"Parameter list: {param_list}")
            logger.info(f"Return type: {return_type}")
            
            # Precompute the joined strings to avoid backslashes in f-string expressions
            input_parsing_code = "\n        ".join(param_parsing)
            function_params = ", ".join(param_list)
            function_call_args = ", ".join([p.split()[-1] for p in param_list])
            
            # Remove any existing class/method declarations from source code
            code_body = re.sub(r'public.*?\{', '', source_code)
            code_body = re.sub(r'\}[\s]*$', '', code_body)
            
            submission_template = """import java.util.*;
import java.util.regex.*;

public class {class_name} {{
    public {return_type} {function_name}({function_params}) {{
{source_code}
    }}

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
            
            # Save the generated Java code to Main.java
            try:
                with open('Main.java', 'w') as f:
                    f.write(submission.strip())
                logger.info("Successfully saved generated Java code to Main.java")
            except Exception as e:
                logger.error(f"Failed to save Main.java: {str(e)}")
            
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
        Validates that the source code contains the expected function name.
        Converts Python-style function name to Java convention before checking.
        """
        # Remove comments and whitespace
        code = re.sub(r'//.*?\n|/\*.*?\*/', '', source_code, flags=re.S)
        code = code.strip()

        # Extract function name and convert to Java convention
        function_name = problem_structure.get("function_name")
        if not function_name:
            raise JavaSubmissionGeneratorException("Missing function name in problem structure")

        # Convert Python snake_case to Java camelCase
        java_function_name = to_java_name(function_name)
        
        logger.info(f"Checking for function name: {java_function_name} (original: {function_name})")

        # Check if the Java-style function name exists in the code
        if java_function_name not in code:
            raise JavaSubmissionGeneratorException(
                f"Function '{java_function_name}' not found in source code"
            )

    def _convert_type_to_java(self, python_type: str) -> str:
        """
        Converts Python type hints to Java type declarations.
        """
        # Convert type to lowercase for case-insensitive matching
        python_type = python_type.lower()
        
        # Handle List types first
        if python_type.startswith("list["):
            inner_type = python_type[5:-1]  # extract type inside List[]
            if inner_type == "int":
                return "int[]"
            elif inner_type == "str" or inner_type == "string":
                return "String[]"
            elif inner_type == "float":
                return "double[]"
            elif inner_type == "bool":
                return "boolean[]"
        
        # Handle simple types
        type_mapping = {
            "str": "String",
            "string": "String",
            "int": "int",
            "float": "double",
            "bool": "boolean"
        }
        
        return type_mapping.get(python_type, "Object")

    def _generate_input_parsing(self, java_type: str, param_name: str, index: int, total_inputs: int) -> str:
        """Generate code to parse input based on type"""
        if java_type.endswith("[]"):
            # When there is only one input field, assume the array may be given on multiple lines.
            if total_inputs == 1:
                if java_type == "int[]":
                    return (
                       f"List<String> lines = new ArrayList<>();\n"
                       f"        while(scanner.hasNextLine()){{\n"
                       f"            String line = scanner.nextLine();\n"
                       f"            if(line.trim().isEmpty()) break;\n"
                       f"            lines.add(line);\n"
                       f"        }}\n"
                       f"        String allInput = String.join(\" \", lines);\n"
                       f"        String[] tokens = allInput.trim().isEmpty() ? new String[0] : allInput.split(\"\\\\s+\");\n"
                       f"        int[] {param_name} = new int[tokens.length];\n"
                       f"        for(int i = 0; i < tokens.length; i++) {{\n"
                       f"            {param_name}[i] = Integer.parseInt(tokens[i]);\n"
                       f"        }}"
                    )
                elif java_type == "String[]":
                    return (
                       f"List<String> lines = new ArrayList<>();\n"
                       f"        while(scanner.hasNextLine()){{\n"
                       f"            String line = scanner.nextLine();\n"
                       f"            if(line.trim().isEmpty()) break;\n"
                       f"            lines.add(line);\n"
                       f"        }}\n"
                       f"        String[] {param_name} = lines.toArray(new String[0]);"
                    )
                elif java_type == "double[]":
                    return (
                       f"List<String> lines = new ArrayList<>();\n"
                       f"        while(scanner.hasNextLine()){{\n"
                       f"            String line = scanner.nextLine();\n"
                       f"            if(line.trim().isEmpty()) break;\n"
                       f"            lines.add(line);\n"
                       f"        }}\n"
                       f"        String allInput = String.join(\" \", lines);\n"
                       f"        String[] tokens = allInput.trim().isEmpty() ? new String[0] : allInput.split(\"\\\\s+\");\n"
                       f"        double[] {param_name} = new double[tokens.length];\n"
                       f"        for(int i = 0; i < tokens.length; i++) {{\n"
                       f"            {param_name}[i] = Double.parseDouble(tokens[i]);\n"
                       f"        }}"
                    )
                else:
                    # Fallback: treat as String[]
                    return (
                       f"List<String> lines = new ArrayList<>();\n"
                       f"        while(scanner.hasNextLine()){{\n"
                       f"            String line = scanner.nextLine();\n"
                       f"            if(line.trim().isEmpty()) break;\n"
                       f"            lines.add(line);\n"
                       f"        }}\n"
                       f"        {java_type} {param_name} = lines.toArray(new String[0]);"
                    )
            else:
                # Multiple input fields – assume input for this field is on one line.
                if java_type == "int[]":
                    return (
                       f"String[] input{index} = scanner.nextLine().split(\" \");\n"
                       f"        int[] {param_name} = new int[input{index}.length];\n"
                       f"        for(int i = 0; i < input{index}.length; i++) {{\n"
                       f"            {param_name}[i] = Integer.parseInt(input{index}[i]);\n"
                       f"        }}"
                    )
                elif java_type == "String[]":
                    return f"String[] {param_name} = scanner.nextLine().split(\" \");"
                elif java_type == "double[]":
                    return (
                       f"String[] input{index} = scanner.nextLine().split(\" \");\n"
                       f"        double[] {param_name} = new double[input{index}.length];\n"
                       f"        for(int i = 0; i < input{index}.length; i++) {{\n"
                       f"            {param_name}[i] = Double.parseDouble(input{index}[i]);\n"
                       f"        }}"
                    )
                else:
                    # Fallback for array types not explicitly handled.
                    return f"String[] {param_name} = scanner.nextLine().split(\" \");"
        else:
            # Non-array types – same as before.
            if java_type == "int":
                return f"int {param_name} = Integer.parseInt(scanner.nextLine());"
            elif java_type == "double":
                return f"double {param_name} = Double.parseDouble(scanner.nextLine());"
            elif java_type == "String":
                return f"String {param_name} = scanner.nextLine();"
            elif java_type == "boolean":
                return f"boolean {param_name} = Boolean.parseBoolean(scanner.nextLine());"
            else:
                return f"String {param_name} = scanner.nextLine();"

    def _generate_output_printing(self, return_type: str, var_name: str) -> str:
        """Generate code to print output based on type"""
        if return_type.endswith("[]"):
            return f"System.out.println(Arrays.toString({var_name}));"
        return f"System.out.println({var_name});"

    def _generate_submission_template(self, class_name: str, return_type: str, 
                                        function_name: str, param_list: list, 
                                        source_code: str, param_parsing: list) -> str:
        """Generate the complete Java submission template"""
        
        # Join the parameters and parsing code
        function_params = ", ".join(param_list)
        input_parsing_code = "\n        ".join(param_parsing)
        function_call_args = ", ".join(p.split()[-1] for p in param_list)
        
        template = f"""import java.util.*;
import java.util.regex.*;

public class {class_name} {{
    public {return_type} {function_name}({function_params}) {{
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
        System.out.println(result);
        
        scanner.close();
    }}
}}"""
        
        return template
