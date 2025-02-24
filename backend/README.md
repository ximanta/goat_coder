# GOAT Coder Backend

A FastAPI-based backend service for an AI-powered programming education platform that generates coding problems, evaluates submissions, and provides intelligent assistance.

## Project Structure
```
backend/
├── main.py                 # Main application entry point
├── submission_generator/   # Code submission generators
│   └── java_submission_generator.py
└── ...
```

## Key Components

### Java Submission Generator
The `JavaSubmissionGenerator` class in `java_submission_generator.py` handles the generation of complete Java submissions by:
- Validating problem structures and source code
- Converting Python types to Java types
- Generating input parsing and output printing code
- Creating a complete Java class with main method for testing

Key features:
- Supports various data types (int, String, arrays)
- Input validation and error handling
- Automatic generation of input parsing code
- Proper output formatting

### Problem Structure Format
Problems are defined using the following structure:
```json
{
  "problem_name": "Problem Name",
  "function_name": "functionName",
  "input_structure": [
    {
      "Input_Field": "type parameterName"
    }
  ],
  "output_structure": {
    "Output_Field": "type returnType"
  }
}
```

### Supported Data Types
- Basic Types:
  - `int` → `int`
  - `str` → `String`
  - `float` → `double`
  - `bool` → `boolean`
- Array Types:
  - `List[int]` → `int[]`
  - `List[str]` → `String[]`
  - `List[float]` → `double[]`
  - `List[bool]` → `boolean[]`

## Error Handling
The system includes comprehensive error handling:
- `JavaSubmissionGeneratorException` for submission-related errors
- Validation of problem structure completeness
- Source code syntax validation
- Input/output type validation

## Usage Example
```python
generator = JavaSubmissionGenerator()
result = generator.generate_submission(source_code, problem_structure)
```

## Contributing
1. Follow the existing code structure
2. Add appropriate error handling
3. Update tests for new features
4. Document changes in this README

## License
[Add your license information here]

