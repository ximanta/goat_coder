from typing import Dict, List

class JavaBoilerplateGenerator:
    TYPE_MAPPING = {
        "List[int]": "int[]",
        "List[float]": "double[]",
        "List[str]": "String[]",
        "List[bool]": "boolean[]",
        "int": "int",
        "float": "double",
        "str": "String",
        "bool": "boolean",
        "string": "String"  # Handle cases where 'string' is used instead of 'str'
    }

    @staticmethod
    def convert_to_java_type(python_type: str) -> str:
        """Convert Python type notation to Java type notation."""
        return JavaBoilerplateGenerator.TYPE_MAPPING.get(python_type, "Object")

    @staticmethod
    def convert_to_java_name(name: str) -> str:
        """Convert Python function name to Java naming convention."""
        # Split by underscore and convert to camelCase
        words = name.split('_')
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @staticmethod
    def parse_input_field(input_field: str) -> tuple:
        """Parse input field string to get type and name."""
        parts = input_field.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Invalid input field format: {input_field}")
        param_type = parts[0]
        param_name = JavaBoilerplateGenerator.convert_to_java_name(parts[1])  # Convert to camelCase
        return param_type, param_name

    @staticmethod
    def is_float_type(type_str: str) -> bool:
        """Check if the type is float/double."""
        return type_str.lower() in ['float', 'double']

    @staticmethod
    def fix_float_values(test_cases: List[Dict], input_types: List[str], output_type: str) -> List[Dict]:
        """Fix float values in test cases to include decimal points."""
        fixed_cases = []
        
        for test_case in test_cases:
            fixed_inputs = []
            # Handle input values
            for i, value in enumerate(test_case['input']):
                # Get the type for this position, use the first type if it's an array
                type_str = input_types[min(i, len(input_types) - 1)]
                
                if JavaBoilerplateGenerator.is_float_type(type_str):
                    # Only convert to float if the type is float/double
                    if isinstance(value, (int, float)):
                        float_value = float(value)
                        # Add .0 only if it's a whole number
                        if float_value.is_integer():
                            value = float(f"{int(float_value)}.0")
                        else:
                            value = float_value
                fixed_inputs.append(value)
            
            # Handle output value
            fixed_output = test_case['output']
            if JavaBoilerplateGenerator.is_float_type(output_type):
                # Only convert to float if the output type is float/double
                if isinstance(fixed_output, (int, float)):
                    float_output = float(fixed_output)
                    # Add .0 only if it's a whole number
                    if float_output.is_integer():
                        fixed_output = float(f"{int(float_output)}.0")
                    else:
                        fixed_output = float_output
            
            fixed_cases.append({
                'input': fixed_inputs,
                'output': fixed_output
            })
        
        return fixed_cases

    @staticmethod
    def convert_to_java_boilerplate(structure: Dict) -> str:
        """Convert problem structure to Java boilerplate code."""
        try:
            # Get function name in Java convention
            function_name = JavaBoilerplateGenerator.convert_to_java_name(
                structure["function_name"]
            )

            # Parse output type
            output_field_key = "Output Field"  # Changed from "Output_Field"
            output_type, _ = JavaBoilerplateGenerator.parse_input_field(
                structure["output_structure"][output_field_key]
            )
            java_output_type = JavaBoilerplateGenerator.convert_to_java_type(output_type)

            # Parse input parameters
            params = []
            input_field_key = "Input Field"  # Being explicit about the key
            for input_field in structure["input_structure"]:
                python_type, param_name = JavaBoilerplateGenerator.parse_input_field(
                    input_field[input_field_key]
                )
                java_type = JavaBoilerplateGenerator.convert_to_java_type(python_type)
                params.append(f"{java_type} {param_name}")

            # Construct the boilerplate
            params_str = ", ".join(params)
            boilerplate = f"""/*DO NOT modify this method.*/
public {java_output_type} {function_name}({params_str}) {{
    // Your implementation code goes here
    
    return null; // Replace with your return statement
}}"""
            
            return boilerplate

        except Exception as e:
            print(f"Structure received: {structure}")  # Add debug logging
            print(f"Error details: {str(e)}")  # Add more detailed error logging
            raise ValueError(f"Failed to generate Java boilerplate: {str(e)}") 