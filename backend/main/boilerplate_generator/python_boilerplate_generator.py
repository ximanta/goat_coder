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
        parts = input_field.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Invalid input field format: {input_field}")
        return parts[0], parts[1]

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