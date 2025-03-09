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
    This class ensures that test case inputs (and outputs) are transformed to the proper format.
    """
    
    def __init__(self):
        pass

    def _is_array_type(self, type_str: str) -> bool:
        """
        Check if a type string represents an array/list type.
        This now includes Java native arrays (e.g., 'int[]').
        """
        logger.debug(f"Checking if type is array: {type_str}")
        return type_str.startswith(("List[", "list[", "Array[", "array[")) or type_str.endswith("[]")

    def _get_base_type(self, type_str: str) -> str:
        """Extract base type from an array/list type."""
        if not self._is_array_type(type_str):
            return type_str
        # Extract type inside brackets for types like List[int]
        start = type_str.find("[") + 1
        end = type_str.rfind("]")
        base_type = type_str[start:end].strip()
        logger.debug(f"Base type for {type_str}: {base_type}")
        return base_type

    def format_test_case_input(self, input_data: Any, input_structure: List[Dict[str, str]]) -> str:
        """
        Format the test case input by transforming array inputs.
        For example, if the input is provided as a multi-line string like:
            "[85, 90, 78, 85, 92, 88]\n85"
        then the first line is converted to:
            "85|90|78|85|92|88"
        so that it can be split in the Java code.
        """
        logger.debug(f"Raw input_data received in format_test_case_input: {input_data}")
        try:
            # Handle empty input
            if not input_data:
                return ""
            
            # --- Case 1: Input provided as a multi-line string ---
            if isinstance(input_data, str) and "\n" in input_data:
                parts = input_data.strip().split("\n")
                logger.debug(f"Split input into parts: {parts}")
                if len(parts) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} lines but got {len(parts)}"
                    )
                processed_parts = []
                for i, part in enumerate(parts):
                    field_type = input_structure[i]["Input_Field"].split()[0]
                    logger.debug(f"Processing part: '{part}' with field type: {field_type}")
                    if self._is_array_type(field_type):
                        part = part.strip()
                        if part.startswith("[") and part.endswith("]"):
                            part = part[1:-1]  # Remove '[' and ']'
                        tokens = [t.strip() for t in part.split(",") if t.strip()]
                        part = "|".join(tokens)
                        logger.debug(f"Transformed array input (string branch): {part}")
                    processed_parts.append(part)
                formatted = "\n".join(processed_parts)
                logger.debug(f"Formatted input_data (string branch): {formatted}")
                return formatted

            # --- Case 2: Single parameter that is an array ---
            if len(input_structure) == 1 and self._is_array_type(input_structure[0]["Input_Field"].split()[0]):
                if isinstance(input_data, (list, tuple)):
                    formatted = "|".join(str(x) for x in input_data)
                    logger.debug(f"Formatted single array input from list: {formatted}")
                    return formatted
                elif isinstance(input_data, str):
                    s = input_data.strip()
                    if s.startswith("[") and s.endswith("]"):
                        s = s[1:-1]
                        tokens = [t.strip() for t in s.split(",") if t.strip()]
                        formatted = "|".join(tokens)
                        logger.debug(f"Formatted single array input from string: {formatted}")
                        return formatted
                    else:
                        return s
                else:
                    return str(input_data)
            
            # --- Case 3: Multiple parameters provided as a list/tuple ---
            if isinstance(input_data, (list, tuple)):
                if len(input_data) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} parameters but got {len(input_data)}"
                    )
                processed_parts = []
                for i, value in enumerate(input_data):
                    field_type = input_structure[i]["Input_Field"].split()[0]
                    logger.debug(f"Processing parameter {i}: {value} with field type: {field_type}")
                    if self._is_array_type(field_type):
                        # If the value is already a list/tuple, join its elements with '|'
                        if isinstance(value, (list, tuple)):
                            part = "|".join(str(x) for x in value)
                        elif isinstance(value, str):
                            s = value.strip()
                            if s.startswith("[") and s.endswith("]"):
                                s = s[1:-1]
                                tokens = [t.strip() for t in s.split(",") if t.strip()]
                                part = "|".join(tokens)
                            else:
                                part = s
                        else:
                            part = str(value)
                        logger.debug(f"Transformed array input (list branch): {part}")
                    else:
                        part = str(value)
                    processed_parts.append(part)
                formatted = "\n".join(processed_parts)
                logger.debug(f"Formatted input_data (list branch): {formatted}")
                return formatted
            
            # --- Case 4: Single parameter provided as a string without newlines ---
            if isinstance(input_data, str):
                values = input_data.strip().split()
                if len(values) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} values but got {len(values)}"
                    )
                formatted = "\n".join(values)
                logger.debug(f"Formatted single line string input: {formatted}")
                return formatted
            
            # Fallback: Convert to string directly
            formatted = str(input_data)
            logger.debug(f"Fallback formatted input: {formatted}")
            return formatted
        
        except Exception as e:
            logger.error(f"Error formatting test case input: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Error formatting test case input: {str(e)}")

    def format_test_case_output(self, output_data: Any, output_structure: Dict[str, str]) -> str:
        """
        Format the expected output as a string.
        This minimal implementation simply converts the output_data to a string.
        """
        try:
            formatted = str(output_data)
            logger.debug(f"Formatted test case output: {formatted}")
            return formatted
        except Exception as e:
            logger.error(f"Error formatting test case output: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Error formatting test case output: {str(e)}")

    def generate_test_cases(self, test_cases: List[Dict[str, Any]], problem_structure: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate formatted test cases for Judge0 submission.
        This function applies the formatting defined in format_test_case_input and
        ensures the expected output is a string.
        """
        logger.debug(f"Raw test_cases received in generate_test_cases: {test_cases}")
        try:
            formatted_cases = []
            for i, test_case in enumerate(test_cases, 1):
                try:
                    formatted_input = self.format_test_case_input(
                        test_case["input"],
                        problem_structure["input_structure"]
                    )
                    # Use "output" if available, otherwise fallback to "expected_output"
                    output_value = test_case.get("output", test_case.get("expected_output"))
                    formatted_output = self.format_test_case_output(
                        output_value,
                        problem_structure["output_structure"]
                    )
                    logger.debug(f"Test case {i} - Formatted input: {formatted_input}")
                    logger.debug(f"Test case {i} - Formatted expected output: {formatted_output}")
                    formatted_cases.append({
                        "input": formatted_input,
                        "expected_output": formatted_output
                    })
                except Exception as e:
                    logger.error(f"Error formatting test case {i}: {str(e)}")
                    raise Judge0TestCaseGeneratorException(f"Test case {i} has invalid format: {str(e)}")
                    
            logger.debug(f"Final formatted test cases: {formatted_cases}")
            return formatted_cases

        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Failed to generate test cases: {str(e)}")
