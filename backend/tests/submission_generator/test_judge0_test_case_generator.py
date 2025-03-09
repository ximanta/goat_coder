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
    This class ensures that test case inputs and outputs are transformed to the proper format.
    """
    
    def __init__(self):
        pass

    def _is_array_type(self, type_str: str) -> bool:
        """
        Check if a type string represents an array/list type.
        This now includes Java native arrays (e.g., 'int[]') and types like "[int]".
        """
        result = (
            type_str.startswith(("List[", "list[", "Array[", "array[")) or 
            type_str.endswith("[]") or 
            (type_str.startswith("[") and type_str.endswith("]"))
        )
        logger.debug(f"_is_array_type('{type_str}') -> {result}")
        return result

    def _get_base_type(self, type_str: str) -> str:
        """
        Extract base type from an array/list type.
        For example, "[double]" or "List[int]" will return "double" and "int", respectively.
        """
        if not self._is_array_type(type_str):
            return type_str
        start = type_str.find("[") + 1
        end = type_str.rfind("]")
        base_type = type_str[start:end].strip()
        logger.debug(f"_get_base_type('{type_str}') -> '{base_type}'")
        return base_type

    def format_test_case_input(self, input_data: Any, input_structure: List[Dict[str, str]]) -> str:
        """
        Format the test case input.
        
        For a single-parameter array, the values are joined with a pipe ("|").
        For multiple parameters, each parameter is processed according to its type and then joined with a newline.
        """
        logger.debug(f"Raw input_data: {input_data}")
        try:
            # Case 1: Single parameter that is an array.
            if len(input_structure) == 1 and self._is_array_type(input_structure[0]["Input_Field"].split()[0]):
                if isinstance(input_data, (list, tuple)):
                    formatted = "|".join(str(x) for x in input_data)
                    logger.debug(f"Formatted single array from list/tuple: {formatted}")
                    return formatted
                elif isinstance(input_data, str):
                    s = input_data.strip()
                    if s.startswith("[") and s.endswith("]"):
                        s = s[1:-1]
                        tokens = [t.strip() for t in s.split(",") if t.strip()]
                        formatted = "|".join(tokens)
                        logger.debug(f"Formatted single array from string: {formatted}")
                        return formatted
                    else:
                        return s
                else:
                    return str(input_data)
            
            # Case 2: Multiple parameters provided as a list/tuple.
            if isinstance(input_data, (list, tuple)):
                if len(input_data) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} values but got {len(input_data)}"
                    )
                processed_parts = []
                for i, value in enumerate(input_data):
                    field_type = input_structure[i]["Input_Field"].split()[0]
                    logger.debug(f"Processing parameter {i}: {value} with field type: {field_type}")
                    if self._is_array_type(field_type):
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
                        processed_parts.append(part)
                    else:
                        processed_parts.append(str(value))
                formatted = "\n".join(processed_parts)
                logger.debug(f"Formatted multiple parameters: {formatted}")
                return formatted

            # Case 3: Input provided as a string with newline(s).
            if isinstance(input_data, str) and "\n" in input_data:
                parts = input_data.strip().split("\n")
                if len(parts) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} lines but got {len(parts)}"
                    )
                processed_parts = []
                for i, part in enumerate(parts):
                    field_type = input_structure[i]["Input_Field"].split()[0]
                    logger.debug(f"Processing line {i}: '{part}' with field type: {field_type}")
                    if self._is_array_type(field_type):
                        part = part.strip()
                        if part.startswith("[") and part.endswith("]"):
                            part = part[1:-1]
                        tokens = [t.strip() for t in part.split(",") if t.strip()]
                        part = "|".join(tokens)
                    processed_parts.append(part)
                formatted = "\n".join(processed_parts)
                logger.debug(f"Formatted multiline string input: {formatted}")
                return formatted

            # Case 4: Input provided as a string without newlines.
            if isinstance(input_data, str):
                values = input_data.strip().split()
                if len(values) != len(input_structure):
                    raise Judge0TestCaseGeneratorException(
                        f"Expected {len(input_structure)} values but got {len(values)}"
                    )
                formatted = "\n".join(values)
                logger.debug(f"Formatted single-line string input: {formatted}")
                return formatted

            # Fallback: Convert to string.
            formatted = str(input_data)
            logger.debug(f"Fallback formatted input: {formatted}")
            return formatted

        except Exception as e:
            logger.error(f"Error formatting test case input: {str(e)}")
            raise Judge0TestCaseGeneratorException(f"Error formatting test case input: {str(e)}")

    def format_test_case_output(self, output_data: Any, output_structure: Dict[str, str]) -> str:
        """
        Format the expected output based on its declared type.
        
        - For array types (e.g. "List[int]"), join elements with a space.
        - For float types, always format as a float (with one decimal point).
        - For boolean types, return "true" or "false" in lowercase.
        - Otherwise, simply convert to string.
        
        Raises an exception if "Output_Field" is missing.
        """
        if "Output_Field" not in output_structure:
            raise Judge0TestCaseGeneratorException("Missing 'Output_Field' in output structure")
        output_type = output_structure["Output_Field"].split()[0]
        logger.debug(f"Output type: {output_type}, output data: {output_data}")
        if self._is_array_type(output_type):
            if isinstance(output_data, (list, tuple)):
                formatted = " ".join(str(x) for x in output_data)
                logger.debug(f"Formatted array output: {formatted}")
                return formatted
            else:
                return str(output_data)
        elif output_type.lower() in ["float", "double"]:
            # Even if an integer is provided, format it as a float.
            formatted = f"{float(output_data):.1f}"
            logger.debug(f"Formatted numeric output (float): {formatted}")
            return formatted
        elif output_type.lower() == "bool":
            formatted = "true" if output_data else "false"
            logger.debug(f"Formatted boolean output: {formatted}")
            return formatted
        else:
            formatted = str(output_data)
            logger.debug(f"Formatted output: {formatted}")
            return formatted

    def generate_test_cases(self, test_cases: List[Dict[str, Any]], problem_structure: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate formatted test cases for Judge0 submission.
        
        Each test case must have an "input" field and either an "output" or "expected_output" field.
        """
        logger.debug(f"Raw test_cases: {test_cases}")
        formatted_cases = []
        for i, test_case in enumerate(test_cases, 1):
            if "input" not in test_case:
                raise Judge0TestCaseGeneratorException("Test case missing 'input' field")
            if "output" not in test_case and "expected_output" not in test_case:
                raise Judge0TestCaseGeneratorException("Test case missing 'output'/'expected_output' field")
            formatted_input = self.format_test_case_input(
                test_case["input"],
                problem_structure["input_structure"]
            )
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
        logger.debug(f"Final formatted test cases: {formatted_cases}")
        return formatted_cases
