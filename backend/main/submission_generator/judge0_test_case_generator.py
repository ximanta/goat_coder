import logging
from typing import Dict, Any, List, Union

# Set up logging
logger = logging.getLogger(__name__)

class Judge0TestCaseGeneratorException(Exception):
    """Custom exception for errors during Judge0 test case generation."""
    pass

class Judge0TestCaseGenerator:
    """
    Handles the generation and formatting of test cases for Judge0 submissions.
    This class is responsible for ensuring test case inputs and outputs follow Judge0's rules.
    """
    
    def __init__(self):
        pass

    def _is_array_type(self, type_str: str) -> bool:
        """Check if a type string represents an array/list type"""
        return type_str.startswith(("List[", "list[", "Array[", "array[", "["))

    def _get_base_type(self, type_str: str) -> str:
        """Extract base type from array/list type"""
        if not self._is_array_type(type_str):
            return type_str
        # Extract type inside List[], Array[], etc.
        start = type_str.find("[") + 1
        end = type_str.rfind("]")
        return type_str[start:end].strip()
        
    def format_test_case_input(self, input_data: Any, input_structure: List[Dict[str, str]]) -> str:
        """
        Format input data based on Judge0's requirements and problem structure.
        Each parameter should be on a new line for proper parsing.
        
        Args:
            input_data: Raw input data (can be string, list, or other types)
            input_structure: List of input field definitions from problem structure
            
        Returns:
            str: Formatted input string ready for Judge0 submission
            
        Raises:
            Judge0TestCaseGeneratorException: If input format is invalid
        """
        try:
            # Handle empty input
            if not input_data:
                return ""

            # For a single input parameter that's an array
            if len(input_structure) == 1 and self._is_array_type(input_structure[0]["Input_Field"].split()[0]):
                # If input is already a list, format it
                if isinstance(input_data, (list, tuple)):
                    # Convert all elements to string and join with spaces
                    return " ".join(str(x) for x in input_data)
                elif isinstance(input_data, str):
                    # Assume string is already space-separated
                    return input_data.strip()
                else:
                    # Single value case
                    return str(input_data)

            # For multiple parameters or non-array inputs
            if isinstance(input_data, (list, tuple)):
                # Validate number of values matches structure
                if len(input_data) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} values but got {len(input_data)}"
                    )
                # Convert each value to string and join with newlines
                return "\n".join(str(x) for x in input_data)
                
            # If input_data is a string
            if isinstance(input_data, str):
                # Split string input into values
                values = input_data.strip().split()
                
                # Validate number of values matches structure
                if len(values) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} values but got {len(values)}"
                    )
                    
                # Join values with newlines
                return "\n".join(values)
                
            # For any other type, convert to string
            return str(input_data)

        except Exception as e:
            logger.error(f"Error formatting test case input: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Error formatting test case input: {str(e)}")
        
    def format_test_case_output(self, output_data: Any, output_structure: Dict[str, str]) -> str:
        """
        Format expected output based on Judge0's requirements and problem structure.
        
        Args:
            output_data: Raw output data
            output_structure: Output field definition from problem structure
            
        Returns:
            str: Formatted output string ready for Judge0 submission
            
        Raises:
            Judge0TestCaseGeneratorException: If output format is invalid
        """
        try:
            # Get output type
            output_type = output_structure["Output_Field"].split()[0]

            # Handle array output types
            if self._is_array_type(output_type):
                if isinstance(output_data, (list, tuple)):
                    return " ".join(str(x) for x in output_data)
                elif isinstance(output_data, str):
                    return output_data.strip()
                else:
                    return str(output_data)

            # Handle float/double types with potential precision issues
            if output_type.lower() in ["float", "double"]:
                if isinstance(output_data, (int, float)):
                    # If it's an integer type or a float with no fractional part:
                    if isinstance(output_data, int) or (isinstance(output_data, float) and output_data.is_integer()):
                        return f"{float(output_data):.1f}"
                    else:
                        # For floats with a fractional part, return the exact value.
                        return str(output_data)
            else:
                return str(output_data)

            # Handle boolean types
            if output_type.lower() == "bool":
                return str(output_data).lower()

            # For all other types, convert to string
            return str(output_data)

        except Exception as e:
            logger.error(f"Error formatting test case output: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Error formatting test case output: {str(e)}")

    def generate_test_cases(self, test_cases: List[Dict[str, Any]], problem_structure: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate formatted test cases for Judge0 submission.
        
        Args:
            test_cases: List of test cases with input and expected output
            problem_structure: Problem structure with input/output definitions
            
        Returns:
            List[Dict[str, str]]: List of formatted test cases ready for Judge0
            
        Raises:
            Judge0TestCaseGeneratorException: If test case generation fails
        """
        try:
            formatted_cases = []
            for i, test_case in enumerate(test_cases, 1):
                try:
                    formatted_input = self.format_test_case_input(
                        test_case["input"],
                        problem_structure["input_structure"]
                    )
                    formatted_output = self.format_test_case_output(
                        test_case["output"],
                        problem_structure["output_structure"]
                    )
                    formatted_cases.append({
                        "input": formatted_input,
                        "expected_output": formatted_output
                    })
                except Exception as e:
                    logger.error(f"Error formatting test case {i}: {str(e)}")
                    raise Judge0TestCaseGeneratorException(f"Test case {i} has invalid format: {str(e)}")
                    
            return formatted_cases

        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Failed to generate test cases: {str(e)}")
