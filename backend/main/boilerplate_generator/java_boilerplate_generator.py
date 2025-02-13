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
        "string": "String",  # Handle cases where 'string' is used instead of 'str'
        # Wrapper types for use in generic types like Dict
        "_wrapper": {
            "int": "Integer",
            "float": "Double",
            "str": "String",
            "string": "String",
            "bool": "Boolean"
        },
        "Dict": "Map",  # Base mapping for Dict type
        "dict": "Map<String, Object>",  # Default mapping for untyped dict
        "Union": "Object",  # Union types fall back to Object
        "Any": "Object"    # Any type falls back to Object
    }

    @staticmethod
    def convert_to_java_name(name: str) -> str:
        """Convert Python function name to Java naming convention."""
        # Split by underscore and convert to camelCase
        words = name.split('_')
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @staticmethod
    def normalize_type(type_str: str) -> str:
        """Normalize type strings to consistent format."""
        # Convert dict[key, value] to Dict[key, value]
        if type_str.lower().startswith("dict["):
            inner_types = type_str[5:-1]  # Remove 'dict[' and ']'
            return f"Dict[{inner_types}]"
        # Convert 'dict' to 'Dict'
        elif type_str.lower() == "dict":
            return "Dict"
        # Handle Union types
        elif "Union[" in type_str:
            return "Union"
        return type_str

    @staticmethod
    def parse_input_field(input_field: str) -> tuple:
        """Parse input field string to get type and name."""
        parts = input_field.strip().split()
        
        # Handle case where only type is provided (common in output_structure)
        if len(parts) == 1:
            param_type = JavaBoilerplateGenerator.normalize_type(parts[0])
            param_name = "result"  # Default name for output parameter
        elif len(parts) == 2:
            param_type = JavaBoilerplateGenerator.normalize_type(parts[0])
            param_name = JavaBoilerplateGenerator.convert_to_java_name(parts[1])
        else:
            raise ValueError(f"Invalid input field format: {input_field}")

        # Handle untyped dict case by providing default type
        if param_type == "Dict":
            # Look at test cases to infer key and value types
            param_type = "Dict[str, int]"  # Default to common case of str->int mapping
            
        return param_type, param_name

    @staticmethod
    def is_float_type(type_str: str) -> bool:
        """Check if the type is float/double."""
        return type_str.lower() in ['float', 'double']

    @staticmethod
    def get_wrapper_type(primitive_type: str) -> str:
        """Get the Java wrapper type for a primitive type."""
        wrapper_map = JavaBoilerplateGenerator.TYPE_MAPPING["_wrapper"]
        return wrapper_map.get(primitive_type, primitive_type)

    @staticmethod
    def parse_complex_type(type_str: str) -> str:
        """Parse complex types like Dict[key_type, value_type] and convert to Java type."""
        if type_str.startswith("Dict["):
            # Extract the key and value types from Dict[key_type, value_type]
            inner_types = type_str[5:-1].split(", ")  # Remove 'Dict[' and ']', then split
            if len(inner_types) == 2:
                key_type = inner_types[0]
                value_type = inner_types[1]
                
                # If value type contains Union or complex types, use Object
                if "Union[" in value_type or "[" in value_type:
                    value_type = "Object"
                else:
                    value_type = JavaBoilerplateGenerator.get_wrapper_type(value_type)
                
                # If key type contains Union or complex types, use String as default
                if "Union[" in key_type or "[" in key_type:
                    key_type = "String"
                else:
                    key_type = JavaBoilerplateGenerator.get_wrapper_type(key_type)
                
                base_type = JavaBoilerplateGenerator.TYPE_MAPPING["Dict"]
                return f"{base_type}<{key_type}, {value_type}>"
        elif "Union[" in type_str:
            return "Object"  # Union types fall back to Object
        return JavaBoilerplateGenerator.TYPE_MAPPING.get(type_str, "Object")

    @staticmethod
    def convert_to_java_type(python_type: str) -> str:
        """Convert Python type notation to Java type notation."""
        if "[" in python_type:  # Handle any complex type with brackets
            if python_type.startswith("List["):
                inner_type = python_type[5:-1]  # Remove 'List[' and ']'
                if "Union[" in inner_type or "Dict[" in inner_type:
                    return "List<Object>"  # Complex inner types fall back to Object
                return JavaBoilerplateGenerator.TYPE_MAPPING.get(python_type, "List<Object>")
            return JavaBoilerplateGenerator.parse_complex_type(python_type)
        return JavaBoilerplateGenerator.TYPE_MAPPING.get(python_type, "Object")

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
            output_field_key = "Output Field"
            output_type, output_name = JavaBoilerplateGenerator.parse_input_field(
                structure["output_structure"][output_field_key]
            )
            
            # Try to infer dict types from test cases if available
            if output_type.startswith("Dict") and "test_cases" in structure:
                first_output = structure["test_cases"][0]["output"]
                if first_output:
                    key_type = type(next(iter(first_output.keys()))).__name__
                    value_type = type(next(iter(first_output.values()))).__name__
                    output_type = f"Dict[{key_type}, {value_type}]"
            
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