import os
import sys
import pytest

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main.submission_generator.java_submission_generator import JavaSubmissionGenerator, JavaSubmissionGeneratorException

@pytest.fixture
def generator():
    return JavaSubmissionGenerator()

def test_validate_problem_structure(generator):
    # Test valid structure
    valid_structure = {
        "problem_name": "Test Problem",
        "function_name": "solve_problem",
        "input_structure": [{"Input_Field": "int x"}],
        "output_structure": {"Output_Field": "int result"}
    }
    generator._validate_problem_structure(valid_structure)  # Should not raise exception
    
    # Test missing fields
    invalid_structures = [
        {},  # Empty structure
        {"problem_name": "Test"},  # Missing other fields
        {
            "problem_name": "Test",
            "function_name": "test",
            "input_structure": []
        }  # Missing output_structure
    ]
    
    for invalid_structure in invalid_structures:
        with pytest.raises(JavaSubmissionGeneratorException):
            generator._validate_problem_structure(invalid_structure)

def test_validate_source_code(generator):
    problem_structure = {
        "function_name": "solve_problem"
    }
    
    # Test valid source code
    valid_source = """
    public int solveProblem(int x) {
        return x * 2;
    }
    """
    generator._validate_source_code(valid_source, problem_structure)  # Should not raise exception
    
    # Test empty source code
    with pytest.raises(JavaSubmissionGeneratorException):
        generator._validate_source_code("", problem_structure)
    
    # Test source code without the expected function
    with pytest.raises(JavaSubmissionGeneratorException):
        generator._validate_source_code("public int wrongFunction() {}", problem_structure)

def test_convert_type_to_java(generator):
    # Test simple types
    assert generator._convert_type_to_java("str") == "String"
    assert generator._convert_type_to_java("int") == "int"
    assert generator._convert_type_to_java("float") == "double"
    assert generator._convert_type_to_java("bool") == "boolean"
    
    # Test array types
    assert generator._convert_type_to_java("list[int]") == "int[]"
    assert generator._convert_type_to_java("list[str]") == "String[]"
    assert generator._convert_type_to_java("list[float]") == "double[]"
    
    # Test dictionary types
    assert generator._convert_type_to_java("dict[str, int]") == "Map<String, int>"
    assert generator._convert_type_to_java("dict[str, list[int]]") == "Map<String, int[]>"
    
    # Test unknown types
    assert generator._convert_type_to_java("unknown_type") == "Object"

def test_generate_input_parsing(generator):
    # Test primitive types
    assert "int x = Integer.parseInt(scanner.nextLine());" in generator._generate_input_parsing("int", "x", 0, 1)
    assert "double y = Double.parseDouble(scanner.nextLine());" in generator._generate_input_parsing("double", "y", 0, 1)
    assert "String s = scanner.nextLine();" in generator._generate_input_parsing("String", "s", 0, 1)
    
    # Test array types
    int_array_parsing = generator._generate_input_parsing("int[]", "nums", 0, 1)
    assert 'String[] numsStr = scanner.nextLine().split(" ");' in int_array_parsing
    assert "int[] nums = new int[numsStr.length];" in int_array_parsing
    assert "Integer.parseInt(numsStr[i])" in int_array_parsing
    
    # Test unsupported types
    with pytest.raises(JavaSubmissionGeneratorException):
        generator._generate_input_parsing("Map<String, Integer>", "map", 0, 1)

def test_parse_array_input(generator):
    # Test string array
    string_array = generator._parse_array_input("String", "words")
    assert 'String[] words = scanner.nextLine().split(" ");' == string_array
    
    # Test int array
    int_array = generator._parse_array_input("int", "nums")
    assert 'String[] numsStr = scanner.nextLine().split(" ");' in int_array
    assert 'int[] nums = new int[numsStr.length];' in int_array
    
    # Test unsupported type
    with pytest.raises(JavaSubmissionGeneratorException):
        generator._parse_array_input("CustomType", "arr")

def test_parse_value(generator):
    assert generator._parse_value("int", "x") == "Integer.parseInt(scanner.nextLine())"
    assert generator._parse_value("double", "d") == "Double.parseDouble(scanner.nextLine())"
    assert generator._parse_value("String", "s") == "scanner.nextLine()"
    assert generator._parse_value("boolean", "b") == "Boolean.parseBoolean(scanner.nextLine())"
    assert generator._parse_value("unknown", "u") == "scanner.nextLine()"

def test_generate_output_printing(generator):
    # Test primitive type
    assert "System.out.println(result);" == generator._generate_output_printing("int", "result")
    
    # Test array type
    array_output = generator._generate_output_printing("int[]", "result")
    assert "StringBuilder sb = new StringBuilder();" in array_output
    assert "System.out.println(sb.toString());" in array_output
    assert "null" in array_output  # Should handle null case

def test_generate_submission(generator):
    source_code = """
    public int addNumbers(int a, int b) {
        return a + b;
    }
    """
    
    problem_structure = {
        "problem_name": "Add Numbers",
        "function_name": "add_numbers",
        "input_structure": [
            {"Input_Field": "int a"},
            {"Input_Field": "int b"}
        ],
        "output_structure": {
            "Output_Field": "int result"
        }
    }
    
    submission = generator.generate_submission(source_code, problem_structure)
    
    # Check essential parts
    assert "public class Main" in submission
    assert "public int addNumbers(int a, int b)" in submission
    assert "Scanner scanner = new Scanner(System.in);" in submission
    assert "Integer.parseInt(scanner.nextLine());" in submission
    assert "System.out.println(result);" in submission
    assert "scanner.close();" in submission

def test_generate_submission_with_arrays(generator):
    source_code = """
    public int[] processArray(int[] nums) {
        int[] result = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            result[i] = nums[i] * 2;
        }
        return result;
    }
    """
    
    problem_structure = {
        "problem_name": "Process Array",
        "function_name": "process_array",
        "input_structure": [
            {"Input_Field": "list[int] nums"}
        ],
        "output_structure": {
            "Output_Field": "list[int] result"
        }
    }
    
    submission = generator.generate_submission(source_code, problem_structure)
    
    # Check array-specific parts
    assert "public int[] processArray(int[] nums)" in submission
    assert 'String[] numsStr = scanner.nextLine().split(" ");' in submission
    assert "StringBuilder sb = new StringBuilder();" in submission
