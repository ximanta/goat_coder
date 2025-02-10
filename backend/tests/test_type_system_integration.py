import pytest
from main.type_system import TypeValidator, TypeConverter, TypeSystemException
from main.problem_generator.problem_generator_service import ProblemGeneratorService
from main.submission_generator.java_submission_generator import JavaSubmissionGenerator

@pytest.fixture
def type_validator():
    return TypeValidator()

@pytest.fixture
def type_converter():
    return TypeConverter()

def test_python_structure_validation(type_validator):
    structure = {
        "input_structure": [
            {"Input Field": "List[int] numbers"}
        ],
        "output_structure": {
            "Output Field": "int result"
        }
    }
    assert type_validator.validate_structure(structure, "python") == True

def test_java_structure_validation(type_validator):
    structure = {
        "input_structure": [
            {"Input Field": "int[] numbers"}
        ],
        "output_structure": {
            "Output Field": "int result"
        }
    }
    assert type_validator.validate_structure(structure, "java") == True

def test_structure_conversion(type_converter):
    python_structure = {
        "input_structure": [
            {"Input Field": "List[int] numbers"}
        ],
        "output_structure": {
            "Output Field": "int result"
        }
    }
    
    java_structure = type_converter.convert_structure(
        python_structure,
        from_lang="python",
        to_lang="java"
    )
    
    assert java_structure["input_structure"][0]["Input Field"] == "int[] numbers"
    assert java_structure["output_structure"]["Output Field"] == "int result"

def test_invalid_type_validation(type_validator):
    invalid_structure = {
        "input_structure": [
            {"Input Field": "invalid_type numbers"}
        ],
        "output_structure": {
            "Output Field": "int result"
        }
    }
    
    with pytest.raises(TypeSystemException):
        type_validator.validate_structure(invalid_structure, "java") 