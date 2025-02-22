from typing import Dict, List, Any, Tuple
from .base_generator import BaseBoilerplateGenerator

class PythonBoilerplateGenerator(BaseBoilerplateGenerator):
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

    def convert_type(self, type_str: str) -> str:
        """Convert generic type to Python type."""
        return self.TYPE_MAPPING.get(type_str, "Any")

    def parse_input_field(self, input_field: str) -> Tuple[str, str]:
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

    def generate_boilerplate(self, structure: Dict) -> str:
        """Generate Python boilerplate code."""
        try:
            # Get function name (Python uses snake_case, so no conversion needed)
            function_name = structure["function_name"]
            
            # Parse output type
            output_type, _ = self.parse_input_field(
                structure["output_structure"]["Output Field"]
            )
            python_output_type = self.convert_type(output_type)

            # Parse input parameters
            params = []
            param_types = []
            for input_field in structure["input_structure"]:
                python_type, param_name = self.parse_input_field(
                    input_field["Input Field"]
                )
                type_hint = self.convert_type(python_type)
                params.append(param_name)
                param_types.append(f"{param_name}: {type_hint}")

            # Generate function definition without imports by default
            boilerplate = f"def {function_name}({', '.join(param_types)}) -> {python_output_type}:\n"
            boilerplate += "    # Write your code here\n"
            boilerplate += "    pass"
            
            return boilerplate
            
        except Exception as e:
            print(f"Structure received: {structure}")  # Add debug logging
            print(f"Error details: {str(e)}")  # Add more detailed error logging
            raise ValueError(f"Failed to generate Python boilerplate: {str(e)}")

    def generate_test_case(self, test_case: Dict, function_name: str) -> str:
        """Generate Python test case."""
        input_values = test_case.get("input", [])
        expected_output = test_case.get("output")
        
        test_case_str = f"""
    def test_{function_name}_case_{test_case.get('id', 1)}(self):
        # Arrange
        {self._format_input_values(input_values)}
        
        # Act
        result = {function_name}({', '.join(f'input{i+1}' for i in range(len(input_values)))})
        
        # Assert
        self.assertEqual({expected_output}, result)
"""
        return test_case_str

    def get_imports(self) -> List[str]:
        """Get required Python imports."""
        # Return an empty list by default - imports will be added only when explicitly needed
        return []

    def _format_input_values(self, input_values: List[Any]) -> str:
        """Format input values for test case."""
        formatted_inputs = []
        for i, value in enumerate(input_values):
            if isinstance(value, list):
                formatted_inputs.append(f"input{i+1} = {value}")
            elif isinstance(value, str):
                formatted_inputs.append(f'input{i+1} = "{value}"')
            else:
                formatted_inputs.append(f"input{i+1} = {value}")
        return "\n        ".join(formatted_inputs)