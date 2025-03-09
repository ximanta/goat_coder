from typing import Dict, List, Any, Tuple
from main.type_mapping_system.java.java_type_mapper import JavaTypeMapper
from main.type_mapping_system.java.java_name_converter import to_java_name
from .base_generator import BaseBoilerplateGenerator

class JavaBoilerplateGenerator(BaseBoilerplateGenerator):
    """Generator for Java boilerplate code."""

    def __init__(self):
        self.type_mapper = JavaTypeMapper()

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
        input_field = input_field.strip()
        
        # Handle case where the type contains spaces within brackets
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
    def is_float_type(type_str: str) -> bool:
        """Check if the type is float/double."""
        return type_str.lower() in ['float', 'double']

    @classmethod
    def get_wrapper_type(cls, primitive_type: str) -> str:
        """Get the Java wrapper type for a primitive type."""
        # Create a temporary instance to use the type_mapper
        instance = cls()
        return instance.type_mapper.get_wrapper_type(primitive_type)

    @classmethod
    def parse_complex_type(cls, type_str: str) -> str:
        """Parse complex types like Dict[key_type, value_type] and convert to Java type."""
        # Create a temporary instance to use the type_mapper
        instance = cls()
        return instance.type_mapper.to_java_type(type_str)

    @classmethod
    def convert_to_java_type(cls, python_type: str) -> str:
        """Convert Python type notation to Java type notation."""
        # Create a temporary instance to use the type_mapper
        instance = cls()
        return instance.type_mapper.to_java_type(python_type)

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
    def infer_type_from_test_cases(structure: Dict, field_type: str) -> str:
        """Infer more specific type information from test cases."""
        if not field_type.startswith("Dict"):
            return field_type
            
        if "test_cases" not in structure:
            return field_type
            
        # For dictionaries, check the first test case
        first_case = structure["test_cases"][0]
        if not first_case:
            return field_type
            
        # For output structure, look at output
        if field_type == "Dict" or field_type.startswith("dict"):
            output_dict = first_case.get("output", {})
            if not output_dict:
                return "Dict[str, Object]"  # Default if no test case data
                
            # Check all values in the dictionary
            value_types = set()
            for value in output_dict.values():
                value_types.add(type(value).__name__)
                
            # If we have mixed types or non-primitive types, use Object
            if len(value_types) > 1 or any(t not in ["int", "float", "str", "bool"] for t in value_types):
                return "Dict[str, Object]"
            
            # If all values are of the same type, use that type
            value_type = next(iter(value_types))
            return f"Dict[str, {value_type}]"
            
        return field_type

    def convert_type(self, type_str: str) -> str:
        """Convert generic type to Java type."""
        return self.type_mapper.to_java_type(type_str)

    def parse_input_field(self, input_field: str) -> Tuple[str, str]:
        """Parse input field string to get type and name."""
        input_field = input_field.strip()
        
        # Handle case where the type contains spaces within brackets
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
        """Generate Java boilerplate code."""
        return self.convert_to_java_boilerplate(structure)

    def convert_to_java_boilerplate(self, structure: Dict) -> str:
        """Convert problem structure to Java boilerplate code."""
        try:
            # Get function name in Java convention
            function_name = to_java_name(structure["function_name"])
            
            # Parse output type
            output_type, _ = self.parse_input_field(
                structure["output_structure"]["Output Field"]
            )
            java_output_type = JavaBoilerplateGenerator.convert_to_java_type(output_type)

            # Parse input parameters
            params = []
            for input_field in structure["input_structure"]:
                java_type, param_name = self.parse_input_field(
                    input_field["Input Field"]
                )
                type_hint = JavaBoilerplateGenerator.convert_to_java_type(java_type)
                # Convert parameter name using the centralized name converter
                java_param_name = to_java_name(param_name)
                params.append(f"{type_hint} {java_param_name}")

            # Construct the boilerplate
            boilerplate = f"""public {java_output_type} {function_name}({", ".join(params)}) {{
    // Your implementation code goes here
    return null;  // Replace with actual return value
}}"""
            return boilerplate

        except Exception as e:
            print(f"Structure received: {structure}")  # Add debug logging
            print(f"Error details: {str(e)}")  # Add more detailed error logging
            raise ValueError(f"Failed to generate Java boilerplate: {str(e)}") 

    def generate_test_case(self, test_case: Dict, function_name: str) -> str:
        """Generate Java test case."""
        # Implementation needed
        input_values = test_case.get("input", [])
        expected_output = test_case.get("output")
        
        test_case_str = f"""
    @Test
    public void test{function_name}Case{test_case.get('id', 1)}() {{
        // Arrange
        {self._format_input_values(input_values)}
        
        // Act
        {self._format_function_call(function_name, input_values)}
        
        // Assert
        assertEquals({expected_output}, result);
    }}
"""
        return test_case_str

    def get_imports(self) -> List[str]:
        """Get required Java imports."""
        return [
            "import java.util.*;",
            "import java.util.stream.*;",
            "import java.io.*;",
            "import org.junit.Test;",
            "import static org.junit.Assert.*;"
        ]

    def _format_input_values(self, input_values: List[Any]) -> str:
        """Format input values for test case."""
        formatted_inputs = []
        for i, value in enumerate(input_values):
            if isinstance(value, list):
                formatted_inputs.append(f"int[] input{i+1} = {str(value).replace('[', '{').replace(']', '}')};")
            elif isinstance(value, str):
                formatted_inputs.append(f'String input{i+1} = "{value}";')
            else:
                formatted_inputs.append(f"{type(value).__name__} input{i+1} = {value};")
        return "\n        ".join(formatted_inputs)

    def _format_function_call(self, function_name: str, input_values: List[Any]) -> str:
        """Format function call for test case."""
        inputs = [f"input{i+1}" for i in range(len(input_values))]
        return f"var result = {function_name}({', '.join(inputs)});"