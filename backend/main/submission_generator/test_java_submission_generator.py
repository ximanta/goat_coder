import os
import re
import pytest

# Import the generator and its exception.
# Adjust the import if your module path is different.
from main.submission_generator.java_submission_generator import JavaSubmissionGenerator, JavaSubmissionGeneratorException

# --- Helper Source Code Strings for Testing ---

# Sample source code for a function that finds unique elements.
FIND_UNIQUE_SOURCE = """
public int[] findUniqueElements(int[] array) {
    // A dummy implementation that simply returns the same array.
    return array;
}
"""

# Sample source code for a function that rotates an array.
ROTATE_ARRAY_SOURCE = """
public int[] rotateArray(int[] array, int k) {
    // A dummy implementation that simply returns the same array.
    return array;
}
"""

# Sample source code for a function that squares an integer.
SQUARE_SOURCE = """
public int square(int x) {
    return x * x;
}
"""

# --- Test Cases ---

def test_single_input_array():
    """
    Test the scenario with a single input field that is an array.
    This simulates a problem like "find_unique_elements" where input is given over multiple lines.
    The generated Java code should use a multi-line reading loop.
    """
    problem_structure = {
        "function_name": "find_unique_elements",
        "input_structure": [
            {"Input_Field": "List[int] array"}
        ],
        "output_structure": {
            "Output_Field": "List[int] result"
        }
    }
    
    generator = JavaSubmissionGenerator()
    submission = generator.generate_submission(FIND_UNIQUE_SOURCE, problem_structure)
    
    # Check that the generated submission contains the multi-line reading code.
    assert "while(scanner.hasNextLine())" in submission, "Expected multi-line input loop not found"
    assert "lines.add(line);" in submission, "Expected adding of lines not found"
    # Check that tokens splitting is handled with an empty-check.
    assert "allInput.trim().isEmpty()" in submission, "Expected check for empty input not found"
    # Also, check that the output printing uses Arrays.toString (because return type is an array).
    assert "Arrays.toString(result)" in submission, "Expected output printing for arrays not found"


def test_multiple_input_fields():
    """
    Test the scenario with multiple input fields.
    For example, the "rotate_array" problem which has two input fields:
    a List[int] array and an int k.
    The generator should produce single-line parsing for the array input.
    """
    problem_structure = {
        "function_name": "rotate_array",
        "input_structure": [
            {"Input_Field": "List[int] array"},
            {"Input_Field": "int k"}
        ],
        "output_structure": {
            "Output_Field": "List[int] result"
        }
    }
    
    generator = JavaSubmissionGenerator()
    submission = generator.generate_submission(ROTATE_ARRAY_SOURCE, problem_structure)
    
    # For multiple input fields, the array input should be read from one line.
    # The generated code should declare a variable like "String line0 = scanner.nextLine();"
    assert re.search(r"String\s+line0\s*=\s*scanner\.nextLine\(\);", submission), "Expected single-line input reading for array not found"
    
    # Also, check that it checks for empty input before splitting.
    assert "trim().isEmpty()" in submission, "Expected empty-line check for array input not found"
    
    # And check that the second input field is parsed correctly.
    assert "int k = Integer.parseInt(scanner.nextLine());" in submission, "Expected parsing for int k not found"


def test_non_array_input():
    """
    Test the scenario with a single input field that is a primitive type (non-array).
    For example, a function that squares an integer.
    """
    problem_structure = {
        "function_name": "square",
        "input_structure": [
            {"Input_Field": "int x"}
        ],
        "output_structure": {
            "Output_Field": "int result"
        }
    }
    
    generator = JavaSubmissionGenerator()
    submission = generator.generate_submission(SQUARE_SOURCE, problem_structure)
    
    # Check that the code uses Integer.parseInt for an int input.
    assert "int x = Integer.parseInt(scanner.nextLine());" in submission, "Expected parsing for int input not found"
    # Since the output is primitive (not an array), output printing should be a direct print.
    assert "System.out.println(result);" in submission, "Expected direct output printing for primitive not found"


def test_invalid_problem_structure_missing_field():
    """
    Test that the generator raises an exception if the problem structure
    is missing a required field (e.g., output_structure).
    """
    # Missing output_structure.
    problem_structure = {
        "function_name": "square",
        "input_structure": [
            {"Input_Field": "int x"}
        ]
        # output_structure is missing
    }
    
    generator = JavaSubmissionGenerator()
    with pytest.raises(JavaSubmissionGeneratorException) as excinfo:
        generator.generate_submission(SQUARE_SOURCE, problem_structure)
    assert "Missing required field" in str(excinfo.value), "Expected missing field error"


def test_invalid_source_code_missing_function():
    """
    Test that the generator raises an exception when the source code
    does not contain the expected function name.
    """
    problem_structure = {
        "function_name": "square",
        "input_structure": [
            {"Input_Field": "int x"}
        ],
        "output_structure": {
            "Output_Field": "int result"
        }
    }
    
    # Source code that does not contain the function "square"
    bad_source = """
    public int notSquare(int x) {
        return x * x;
    }
    """
    
    generator = JavaSubmissionGenerator()
    with pytest.raises(JavaSubmissionGeneratorException) as excinfo:
        generator.generate_submission(bad_source, problem_structure)
    assert "Function 'square'" in str(excinfo.value), "Expected error for missing function name"


def test_generated_file_saved(tmp_path):
    """
    Test that the generated submission file is saved as 'Main.java'.
    We use pytest's tmp_path fixture to change the working directory temporarily.
    """
    # Change directory to a temporary directory.
    os.chdir(tmp_path)
    
    problem_structure = {
        "function_name": "square",
        "input_structure": [
            {"Input_Field": "int x"}
        ],
        "output_structure": {
            "Output_Field": "int result"
        }
    }
    
    generator = JavaSubmissionGenerator()
    submission = generator.generate_submission(SQUARE_SOURCE, problem_structure)
    
    # Check that the file Main.java exists and contains the submission.
    main_file = tmp_path / "Main.java"
    assert main_file.exists(), "Main.java file was not created"
    content = main_file.read_text()
    assert "public class Main" in content, "Main.java does not contain expected class declaration"


def test_empty_line_for_multiple_input_array():
    """
    Test that for multiple input fields, an empty line is handled correctly.
    The generated code should check if the input line is empty and assign an empty array.
    """
    problem_structure = {
        "function_name": "rotate_array",
        "input_structure": [
            {"Input_Field": "List[int] array"},
            {"Input_Field": "int k"}
        ],
        "output_structure": {
            "Output_Field": "List[int] result"
        }
    }
    
    generator = JavaSubmissionGenerator()
    submission = generator.generate_submission(ROTATE_ARRAY_SOURCE, problem_structure)
    
    # Look for the code that checks for an empty line.
    pattern = r"line0\.trim\(\)\.isEmpty\(\)\s*\?\s*new String\[0\]"
    assert re.search(pattern, submission), "Expected empty input check for array field in multiple input case not found"
