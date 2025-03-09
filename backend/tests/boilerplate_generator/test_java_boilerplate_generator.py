import os
import sys
import pytest

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main.boilerplate_generator.java_boilerplate_generator import JavaBoilerplateGenerator

@pytest.fixture
def generator():
    return JavaBoilerplateGenerator()

def test_convert_to_java_name():
    assert JavaBoilerplateGenerator.convert_to_java_name("hello_world") == "helloWorld"
    assert JavaBoilerplateGenerator.convert_to_java_name("calculate_sum") == "calculateSum"
    assert JavaBoilerplateGenerator.convert_to_java_name("get") == "get"
    assert JavaBoilerplateGenerator.convert_to_java_name("") == ""

def test_normalize_type():
    assert JavaBoilerplateGenerator.normalize_type("dict[str, int]") == "Dict[str, int]"
    assert JavaBoilerplateGenerator.normalize_type("dict") == "Dict"
    assert JavaBoilerplateGenerator.normalize_type("Union[str, int]") == "Union"
    assert JavaBoilerplateGenerator.normalize_type("List[int]") == "List[int]"

def test_parse_input_field(generator):
    # Test simple types
    assert generator.parse_input_field("int x") == ("int", "x")
    assert generator.parse_input_field("str") == ("str", "result")
    
    # Test complex types
    assert generator.parse_input_field("List[int] numbers") == ("List[int]", "numbers")
    assert generator.parse_input_field("Dict[str, int] mapping") == ("Dict[str, int]", "mapping")
    
    # Test with default name
    assert generator.parse_input_field("int") == ("int", "result")
    
    # Test error case
    with pytest.raises(ValueError):
        generator.parse_input_field("int x y")

def test_is_float_type():
    assert JavaBoilerplateGenerator.is_float_type("float") == True
    assert JavaBoilerplateGenerator.is_float_type("double") == True
    assert JavaBoilerplateGenerator.is_float_type("FLOAT") == True
    assert JavaBoilerplateGenerator.is_float_type("int") == False
    assert JavaBoilerplateGenerator.is_float_type("str") == False

def test_get_wrapper_type():
    assert JavaBoilerplateGenerator.get_wrapper_type("int") == "Integer"
    assert JavaBoilerplateGenerator.get_wrapper_type("float") == "Double"
    assert JavaBoilerplateGenerator.get_wrapper_type("str") == "String"
    assert JavaBoilerplateGenerator.get_wrapper_type("bool") == "Boolean"
    assert JavaBoilerplateGenerator.get_wrapper_type("unknown") == "unknown"

def test_parse_complex_type():
    # Test dictionary types
    assert JavaBoilerplateGenerator.parse_complex_type("Dict[str, int]") == "Map<String, Integer>"
    # Union types fall back to Object
    assert JavaBoilerplateGenerator.parse_complex_type("Dict[str, Union[int, str]]") == "Object"
    
    # Test Union types
    assert JavaBoilerplateGenerator.parse_complex_type("Union[str, int]") == "Object"
    
    # Test simple types
    assert JavaBoilerplateGenerator.parse_complex_type("int") == "int"

def test_convert_to_java_type():
    # Test array types
    assert JavaBoilerplateGenerator.convert_to_java_type("List[int]") == "int[]"
    assert JavaBoilerplateGenerator.convert_to_java_type("List[str]") == "String[]"
    assert JavaBoilerplateGenerator.convert_to_java_type("List[Union[str, int]]") == "List<Object>"
    
    # Test primitive types
    assert JavaBoilerplateGenerator.convert_to_java_type("int") == "int"
    assert JavaBoilerplateGenerator.convert_to_java_type("str") == "String"
    assert JavaBoilerplateGenerator.convert_to_java_type("float") == "double"
    
    # Test complex types
    assert JavaBoilerplateGenerator.convert_to_java_type("Dict[str, int]") == "Map<String, Integer>"
    assert JavaBoilerplateGenerator.convert_to_java_type("unknown") == "Object"

def test_infer_type_from_test_cases(generator):
    # Test with empty structure
    assert JavaBoilerplateGenerator.infer_type_from_test_cases({}, "Dict") == "Dict"
    
    # Test with non-Dict type
    assert JavaBoilerplateGenerator.infer_type_from_test_cases({}, "int") == "int"
    
    # Test with test cases
    structure = {
        "test_cases": [
            {"output": {"key1": 1, "key2": 2}},
        ]
    }
    assert JavaBoilerplateGenerator.infer_type_from_test_cases(structure, "Dict") == "Dict[str, int]"
    
    # Test with mixed types
    structure = {
        "test_cases": [
            {"output": {"key1": 1, "key2": "str"}},
        ]
    }
    assert JavaBoilerplateGenerator.infer_type_from_test_cases(structure, "Dict") == "Dict[str, Object]"

def test_fix_float_values():
    test_cases = [
        {"input": [1, 2.5], "output": 3},
        {"input": [1.0, 2], "output": 3.5}
    ]
    input_types = ["float", "float"]
    output_type = "float"
    
    fixed_cases = JavaBoilerplateGenerator.fix_float_values(test_cases, input_types, output_type)
    
    # Check first test case
    assert fixed_cases[0]["input"][0] == 1.0
    assert fixed_cases[0]["input"][1] == 2.5
    assert fixed_cases[0]["output"] == 3.0
    
    # Check second test case
    assert fixed_cases[1]["input"][0] == 1.0
    assert fixed_cases[1]["input"][1] == 2.0
    assert fixed_cases[1]["output"] == 3.5

def test_convert_to_java_boilerplate(generator):
    structure = {
        "function_name": "calculate_sum",
        "input_structure": [
            {"Input Field": "int a"},
            {"Input Field": "int b"}
        ],
        "output_structure": {
            "Output Field": "int result"
        }
    }
    
    expected_boilerplate = """public int calculateSum(int a, int b) {
    // Your implementation code goes here
    return null;  // Replace with actual return value
}"""
    
    assert generator.convert_to_java_boilerplate(structure).strip() == expected_boilerplate.strip()

def test_generate_test_case(generator):
    test_case = {
        "id": 1,
        "input": [5, 3],
        "output": 8
    }
    function_name = "calculateSum"
    
    expected_test = """
    @Test
    public void testcalculateSumCase1() {
        // Arrange
        int input1 = 5;
        int input2 = 3;
        
        // Act
        var result = calculateSum(input1, input2);
        
        // Assert
        assertEquals(8, result);
    }
"""
    
    actual_test = generator.generate_test_case(test_case, function_name)
    # Normalize whitespace for comparison
    expected_lines = [line.strip() for line in expected_test.strip().splitlines()]
    actual_lines = [line.strip() for line in actual_test.strip().splitlines()]
    assert actual_lines == expected_lines

def test_get_imports(generator):
    imports = generator.get_imports()
    assert "import java.util.*;" in imports
    assert "import java.util.stream.*;" in imports
    assert "import java.io.*;" in imports
    assert "import org.junit.Test;" in imports
    assert "import static org.junit.Assert.*;" in imports

def test_format_input_values(generator):
    input_values = [42, "hello", [1, 2, 3]]
    expected_output = """int input1 = 42;
        String input2 = "hello";
        int[] input3 = {1, 2, 3};"""
    
    assert generator._format_input_values(input_values).strip() == expected_output.strip()

def test_format_function_call(generator):
    function_name = "calculateSum"
    input_values = [5, 3]
    expected = "var result = calculateSum(input1, input2);"
    
    assert generator._format_function_call(function_name, input_values) == expected
