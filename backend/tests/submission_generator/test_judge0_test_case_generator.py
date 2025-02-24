import pytest
from main.submission_generator.judge0_test_case_generator import Judge0TestCaseGenerator, Judge0TestCaseGeneratorException

@pytest.fixture
def generator():
    return Judge0TestCaseGenerator()

def test_is_array_type(generator):
    # Test various array type formats
    assert generator._is_array_type("List[int]") is True
    assert generator._is_array_type("list[str]") is True
    assert generator._is_array_type("Array[float]") is True
    assert generator._is_array_type("array[double]") is True
    assert generator._is_array_type("[int]") is True
    
    # Test non-array types
    assert generator._is_array_type("int") is False
    assert generator._is_array_type("string") is False
    assert generator._is_array_type("float") is False

def test_get_base_type(generator):
    # Test array type base extraction
    assert generator._get_base_type("List[int]") == "int"
    assert generator._get_base_type("list[str]") == "str"
    assert generator._get_base_type("Array[float]") == "float"
    assert generator._get_base_type("[double]") == "double"
    
    # Test non-array types
    assert generator._get_base_type("int") == "int"
    assert generator._get_base_type("string") == "string"

def test_format_test_case_input_array(generator):
    # Test array input formatting
    input_structure = [{"Input_Field": "List[int] nums"}]
    
    # Test list input
    assert generator.format_test_case_input([1, 2, 3], input_structure) == "1 2 3"
    
    # Test tuple input
    assert generator.format_test_case_input((4, 5, 6), input_structure) == "4 5 6"
    
    # Test string input
    assert generator.format_test_case_input("7 8 9", input_structure) == "7 8 9"
    
    # Test single value
    assert generator.format_test_case_input(10, input_structure) == "10"

def test_format_test_case_input_multiple_params(generator):
    input_structure = [
        {"Input_Field": "int x"},
        {"Input_Field": "int y"}
    ]
    
    # Test list input
    assert generator.format_test_case_input([1, 2], input_structure) == "1\n2"
    
    # Test string input
    assert generator.format_test_case_input("1 2", input_structure) == "1\n2"
    
    # Test invalid number of parameters
    with pytest.raises(Judge0TestCaseGeneratorException):
        generator.format_test_case_input([1], input_structure)
    
    with pytest.raises(Judge0TestCaseGeneratorException):
        generator.format_test_case_input([1, 2, 3], input_structure)

def test_format_test_case_output_array(generator):
    output_structure = {"Output_Field": "List[int] result"}
    
    # Test list output
    assert generator.format_test_case_output([1, 2, 3], output_structure) == "1 2 3"
    
    # Test tuple output
    assert generator.format_test_case_output((4, 5, 6), output_structure) == "4 5 6"
    
    # Test string output
    assert generator.format_test_case_output("7 8 9", output_structure) == "7 8 9"

def test_format_test_case_output_numeric(generator):
    # Test integer output
    int_structure = {"Output_Field": "int result"}
    assert generator.format_test_case_output(42, int_structure) == "42"
    
    # Test float output
    float_structure = {"Output_Field": "float result"}
    assert generator.format_test_case_output(3.14, float_structure) == "3.14"
    assert generator.format_test_case_output(5.0, float_structure) == "5.0"
    assert generator.format_test_case_output(5, float_structure) == "5.0"

def test_format_test_case_output_boolean(generator):
    bool_structure = {"Output_Field": "bool result"}
    
    # Test boolean values
    assert generator.format_test_case_output(True, bool_structure) == "true"
    assert generator.format_test_case_output(False, bool_structure) == "false"

def test_generate_test_cases(generator):
    problem_structure = {
        "input_structure": [
            {"Input_Field": "int x"},
            {"Input_Field": "int y"}
        ],
        "output_structure": {
            "Output_Field": "int result"
        }
    }
    
    test_cases = [
        {"input": [1, 2], "output": 3},
        {"input": [4, 5], "output": 9}
    ]
    
    expected_result = [
        {"input": "1\n2", "expected_output": "3"},
        {"input": "4\n5", "expected_output": "9"}
    ]
    
    result = generator.generate_test_cases(test_cases, problem_structure)
    assert result == expected_result

def test_generate_test_cases_with_arrays(generator):
    problem_structure = {
        "input_structure": [
            {"Input_Field": "List[int] nums"}
        ],
        "output_structure": {
            "Output_Field": "List[int] result"
        }
    }
    
    test_cases = [
        {"input": [1, 2, 3], "output": [2, 4, 6]},
        {"input": [4, 5, 6], "output": [8, 10, 12]}
    ]
    
    expected_result = [
        {"input": "1 2 3", "expected_output": "2 4 6"},
        {"input": "4 5 6", "expected_output": "8 10 12"}
    ]
    
    result = generator.generate_test_cases(test_cases, problem_structure)
    assert result == expected_result

def test_error_handling(generator):
    # Test invalid input structure
    with pytest.raises(Judge0TestCaseGeneratorException):
        generator.format_test_case_input(
            [1, 2],
            [{"Input_Field": "int x"}]  # Mismatch between input length and structure
        )
    
    # Test missing output structure field
    with pytest.raises(Judge0TestCaseGeneratorException):
        generator.format_test_case_output(
            42,
            {}  # Empty output structure should raise error
        )
    
    # Test invalid test case format
    with pytest.raises(Judge0TestCaseGeneratorException):
        generator.generate_test_cases(
            [{"invalid": "format"}],  # Missing required input/output fields
            {"input_structure": [], "output_structure": {}}
        )
