# Backend

A FastAPI-based backend service for an AI-powered programming education platform that generates coding problems, evaluates submissions, and provides intelligent assistance.

## Project Structure
```
backend/
Directory structure:
└── backend/
├── README.md
├── app.py
├── environment.yml
├── last_submission.json
├── main.py
├── requirements.txt
├── __pycache__/
├── debug/
│ ├── Main.java
│ └── last_submission.json
├── main/
│ ├── __init__.py
│ ├── problem_generator.zip
│ ├── __pycache__/
│ ├── boilerplate_generator/
│ │ ├── base_generator.py
│ │ ├── generator_factory.py
│ │ ├── java_boilerplate_generator.py
│ │ ├── python_boilerplate_generator.py
│ │ └── __pycache__/
│ ├── codeassist_chat/
│ │ ├── codeassist_chat_router.py
│ │ ├── codeassist_chat_service.py
│ │ └── __pycache__/
│ ├── problem_generator/
│ │ ├── problem_generator_route.py
│ │ ├── problem_generator_service.py
│ │ ├── prompt_manager.py
│ │ ├── __pycache__/
│ │ └── prompts/
│ │ ├── README.md
│ │ ├── complexity/
│ │ │ ├── easy.md
│ │ │ ├── hard.md
│ │ │ └── medium.md
│ │ ├── concepts/
│ │ │ ├── algorithms_basic/
│ │ │ │ └── config.json
│ │ │ ├── array/
│ │ │ │ └── config.json
│ │ │ ├── array_search/
│ │ │ │ └── config.json
│ │ │ ├── basic_programming_absolute_beginners/
│ │ │ │ └── config.json
│ │ │ └── p1-c2-s4/
│ │ │ └── config.json
│ │ ├── contexts/
│ │ │ ├── easy_contexts.md
│ │ │ ├── hard_contexts.md
│ │ │ └── medium_contexts.md
│ │ └── type_system_old/
│ │ ├── config.json
│ │ ├── constraints.md
│ │ ├── languages/
│ │ │ ├── java_types.json
│ │ │ └── python_types.json
│ │ └── templates/
│ │ ├── function_signatures.json
│ │ └── type_conversions.json
│ ├── problem_submission/
│ │ ├── problem_submission_route.py
│ │ ├── problem_submission_service.py
│ │ └── __pycache__/
│ ├── shared/
│ │ ├── rate_limiter.py
│ │ └── __pycache__/
│ ├── submission_generator/
│ │ ├── __init__.py
│ │ ├── java_submission_generator.py
│ │ ├── judge0_test_case_generator.py
│ │ ├── python_submission_generator.py
│ │ ├── test_java_submission_generator.py
│ │ └── __pycache__/
│ ├── type_system/
│ │ ├── __init__.py
│ │ ├── exceptions.py
│ │ ├── __pycache__/
│ │ ├── config/
│ │ │ ├── __init__.py
│ │ │ ├── java_types.json
│ │ │ ├── python_types.json
│ │ │ └── type_conversions.json
│ │ ├── converters/
│ │ │ ├── __init__.py
│ │ │ ├── type_converter.py
│ │ │ └── __pycache__/
│ │ └── validators/
│ │ ├── __init__.py
│ │ ├── type_validator.py
│ │ └── __pycache__/
│ └── utils/
│ ├── name_converter.py
│ └── __pycache__/
└── tests/
└── test_type_system_integration.py

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


---

## Key Components

### FastAPI Application (main.py)
- **Entry Point:** Initializes FastAPI, sets up middleware (CORS, rate limiting), registers routes for problem generation, code submission, and chat assistance.
- **Logging:** Uses rotating file logging and stream logging to capture runtime events.

### Submission Generators
- **Java Submission Generator:**  
  - Validates the problem structure and user source code.
  - Converts Python‑style function names and types to Java conventions.
  - Generates a full Java class (including `main` method) that parses input and prints output.
- **Judge0 Test Case Generator:**  
  - Formats test cases according to Judge0’s requirements (handles base64 encoding and input/output formatting).

### Problem Generation
- **Prompt Manager:** Loads prompt files (for concepts, complexity, contexts) from disk and selects a randomized prompt configuration.
- **Problem Generator Service:** Uses Azure OpenAI (via `AzureChatOpenAI`) to generate a complete programming problem (including a structured JSON output, test cases, and boilerplate code).

### Code Assistance Chat
- **Chat Service:**  
  - Uses AzureChatOpenAI to stream chat responses based on contextual prompts.
  - Maintains conversation history and caches responses to avoid repeated queries.
- **Chat Router:**  
  - Exposes a streaming endpoint with rate limiting to handle chat requests from the frontend.

### Type System Utilities
TO-DO

### Rate Limiting
- **Shared Rate Limiter:**  
  - Uses SlowAPI to enforce rate limits (e.g., 3 requests per minute on the chat endpoint).

---

## Environment Setup

### Conda Environment
Use the provided `environment.yml` to create the conda environment:
```bash
conda env create -f environment.yml
conda activate goat_coder_env
uvicorn app:app --reload



## Contributing
1. Follow the existing code structure
2. Add appropriate error handling
3. Update tests for new features
4. Document changes in this README



