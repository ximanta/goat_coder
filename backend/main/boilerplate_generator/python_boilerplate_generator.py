from typing import Dict

class PythonBoilerplateGenerator:
    TYPE_MAPPING = {
        "List[int]": "List[int]",
        "List[float]": "List[float]",
        "List[str]": "List[str]",
        "List[bool]": "List[bool]",
        "int": "int",
        "float": "float",
        "str": "str",
        "bool": "bool",
        "string": "str"  # Handle cases where 'string' is used instead of 'str'
    }

    @staticmethod
    def convert_to_python_type(type_str: str) -> str:
        """Convert type notation to Python type hint notation."""
        return PythonBoilerplateGenerator.TYPE_MAPPING.get(type_str, "Any")

    @staticmethod
    def parse_input_field(input_field: str) -> tuple:
        """Parse input field string to get type and name."""
        input_field = input_field.strip()
        
        # Handle case where the type contains spaces within brackets
        # e.g., "List[List[Union[str, int]]] items1" or "Dict[str, int] result"
        if '[' in input_field:
            # Find the last closing bracket
            last_bracket = input_field.rindex(']')
            # Split after the last bracket
            type_part = input_field[:last_bracket + 1]
            name_part = input_field[last_bracket + 1:].strip()
            
            # If no name provided, use default
            if not name_part:
                name_part = "result"
                
            return type_part, name_part
        
        # Handle simple types without brackets
        parts = input_field.split()
        if len(parts) == 1:
            return parts[0], "result"
        elif len(parts) == 2:
            return parts[0], parts[1]
        else:
            raise ValueError(f"Invalid input field format: {input_field}")

    @staticmethod
    def convert_to_python_boilerplate(structure: Dict) -> str:
        """Convert problem structure to Python boilerplate code."""
        try:
            # Get function name (Python uses snake_case, so no conversion needed)
            function_name = structure["function_name"]

            # Parse output type
            output_type, _ = PythonBoilerplateGenerator.parse_input_field(
                structure["output_structure"]["Output Field"]
            )
            python_output_type = PythonBoilerplateGenerator.convert_to_python_type(output_type)

            # Parse input parameters
            params = []
            param_types = []
            for input_field in structure["input_structure"]:
                python_type, param_name = PythonBoilerplateGenerator.parse_input_field(
                    input_field["Input Field"]
                )
                type_hint = PythonBoilerplateGenerator.convert_to_python_type(python_type)
                params.append(param_name)
                param_types.append(f"{param_name}: {type_hint}")

            # Construct the boilerplate with type hints
            params_str = ", ".join(param_types)
            boilerplate = f"""from typing import List

def {function_name}({params_str}) -> {python_output_type}:
    # Your implementation code goes here
    pass"""
            
            return boilerplate

        except Exception as e:
            print(f"Structure received: {structure}")  # Add debug logging
            print(f"Error details: {str(e)}")  # Add more detailed error logging
            raise ValueError(f"Failed to generate Python boilerplate: {str(e)}") 