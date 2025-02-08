import unittest
from main.submission_generator.java_submission_generator import JavaSubmissionGenerator

class TestJavaSubmissionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = JavaSubmissionGenerator()

    def test_array_operation_submission(self):
        # Test case for array operation problem
        source_code = """
            if (operation.equals("insert")) {
                int[] newArray = new int[array.length + 1];
                System.arraycopy(array, 0, newArray, 0, array.length);
                newArray[array.length] = element;
                return newArray;
            }
            return array;
        """
        
        problem_structure = {
            "problem_name": "Array Operation Based on Command",
            "function_name": "array_operation",
            "input_structure": [
                {"Input_Field": "List[int] array"},
                {"Input_Field": "str operation"},
                {"Input_Field": "int element"}
            ],
            "output_structure": {
                "Output_Field": "List[int] result"
            }
        }

        expected_output = """import java.util.*;

public class Solution {
    public int[] array_operation(int[] array, String operation, int element) {
            if (operation.equals("insert")) {
                int[] newArray = new int[array.length + 1];
                System.arraycopy(array, 0, newArray, 0, array.length);
                newArray[array.length] = element;
                return newArray;
            }
            return array;
        
    }
}"""

        generated_code = self.generator.generate_submission(source_code, problem_structure)
        self.assertEqual(generated_code.replace(" ", ""), expected_output.replace(" ", ""))

    def test_type_conversion(self):
        # Test various type conversions
        test_cases = [
            ("str", "String"),
            ("int", "int"),
            ("List[int]", "int[]"),
            ("List[str]", "String[]"),
            ("unknown_type", "Object")  # Default case
        ]

        for python_type, expected_java_type in test_cases:
            with self.subTest(python_type=python_type):
                result = self.generator._convert_type_to_java(python_type)
                self.assertEqual(result, expected_java_type)

    def test_empty_source_code(self):
        # Test with empty source code
        problem_structure = {
            "function_name": "test_function",
            "input_structure": [
                {"Input_Field": "int number"}
            ],
            "output_structure": {
                "Output_Field": "int result"
            }
        }

        generated_code = self.generator.generate_submission("", problem_structure)
        expected_output = """public class Solution {
    public int test_function(int number) {
        
    }
}"""
        self.assertEqual(generated_code.replace(" ", ""), expected_output.replace(" ", ""))

    def test_includes_required_imports(self):
        # Test that generated code includes required imports
        problem_structure = {
            "function_name": "test_function",
            "input_structure": [
                {"Input_Field": "int number"}
            ],
            "output_structure": {
                "Output_Field": "int result"
            }
        }

        generated_code = self.generator.generate_submission("return 0;", problem_structure)
        self.assertIn("import java.util.*;", generated_code)

if __name__ == '__main__':
    unittest.main() 