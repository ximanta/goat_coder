import os
import json
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field
from ..boilerplate_generator.java_boilerplate_generator import JavaBoilerplateGenerator
from ..boilerplate_generator.python_boilerplate_generator import PythonBoilerplateGenerator

class TestCase(BaseModel):
    input: List[Any] = Field(description="Input values for the test case")
    output: Any = Field(description="Expected output for the test case")

class InputField(BaseModel):
    Input_Field: str = Field(description="Type and name of the input parameter", alias="Input Field")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class OutputField(BaseModel):
    Output_Field: str = Field(description="Type and name of the output", alias="Output Field")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ProblemStructure(BaseModel):
    problem_name: str = Field(description="Name of the problem")
    function_name: str = Field(description="Name of the function to implement")
    input_structure: List[InputField] = Field(description="List of input parameters and their types")
    output_structure: OutputField = Field(description="Output parameter and its type")

class Problem(BaseModel):
    concept: str = Field(description="The programming concept being tested")
    difficulty: str = Field(description="Difficulty level of the problem")
    problem_title: str = Field(description="Title of the problem")
    problem_statement: str = Field(description="Detailed problem statement in markdown")
    test_cases: List[TestCase] = Field(description="List of test cases")
    tags: List[str] = Field(description="Tags for the problem")
    structure: ProblemStructure = Field(description="Structure of the problem")
    java_boilerplate: str = Field(description="Java boilerplate code for the problem")
    python_boilerplate: str = Field(description="Python boilerplate code for the problem")

class ProblemGeneratorService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
        )
        self.java_generator = JavaBoilerplateGenerator()
        self.python_generator = PythonBoilerplateGenerator()

    async def generate_problem(self, concept: str, complexity: str) -> Dict:
        messages = [
            {
                "role": "system",
                "content": """You are a programming problem generator. Generate a programming problem based on the given concept 
                and complexity. The problem should be suitable for a hackathon setting.

                IMPORTANT: The problem's input and output must ONLY use these simple types:
                - int
                - float
                - str (string)
                - bool
                - List[int]
                - List[float]
                - List[str]
                - List[bool]

                Do NOT generate problems that require:
                - Multiple function calls
                - Class implementations
                - Complex data structures
                - State management

                Each test case should have:
                - input: A list containing the input values (matching the function parameters)
                - output: A single value of the expected return type

                Example test case formats:
                - For f(x: int) -> int:
                  {"input": [5], "output": 10}
                - For f(arr: List[int], target: int) -> bool:
                  {"input": [[1, 2, 3], 2], "output": true}

                The problem structure should follow this format:
                {
                    "problem_name": "Problem Name",
                    "function_name": "function_name",
                    "input_structure": [
                        {
                            "Input Field": "List[int] array"
                        },
                        {
                            "Input Field": "string operation"
                        },
                        {
                            "Input Field": "int element"
                        }
                    ],
                    "output_structure": {
                        "Output Field": "List[int] result"
                    }
                }

                Format the problem statement in markdown with:
                - Clear title and description
                - Detailed examples with input and output
                - Edge cases in test cases
                - Appropriate function name and parameter types
                - Relevant tags for categorization"""
            },
            {
                "role": "user",
                "content": f"Generate a {complexity} difficulty problem about {concept}"
            }
        ]

        functions = [{
            "name": "generate_programming_problem",
            "description": "Generate a programming problem with specific structure",
            "parameters": {
                "type": "object",
                "properties": {
                    "concept": {"type": "string"},
                    "difficulty": {"type": "string"},
                    "problem_title": {"type": "string"},
                    "problem_statement": {"type": "string"},
                    "test_cases": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "array",
                                    "description": "List of input values matching function parameters. Each value must be one of: int, float, str, bool, or arrays of these types",
                                    "items": {
                                        "oneOf": [
                                            {"type": "integer"},
                                            {"type": "number"},
                                            {"type": "string"},
                                            {"type": "boolean"},
                                            {
                                                "type": "array",
                                                "items": {
                                                    "oneOf": [
                                                        {"type": "integer"},
                                                        {"type": "number"},
                                                        {"type": "string"},
                                                        {"type": "boolean"}
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                                "output": {
                                    "description": "Expected output value of one of the allowed types: int, float, str, bool, or arrays of these types",
                                    "oneOf": [
                                        {"type": "integer"},
                                        {"type": "number"},
                                        {"type": "string"},
                                        {"type": "boolean"},
                                        {
                                            "type": "array",
                                            "items": {
                                                "oneOf": [
                                                    {"type": "integer"},
                                                    {"type": "number"},
                                                    {"type": "string"},
                                                    {"type": "boolean"}
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            "required": ["input", "output"]
                        }
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "structure": {
                        "type": "object",
                        "properties": {
                            "problem_name": {"type": "string"},
                            "function_name": {"type": "string"},
                            "input_structure": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "Input Field": {
                                            "type": "string",
                                            "description": "Type and name of the input parameter (e.g., 'List[int] array', 'string operation')"
                                        }
                                    },
                                    "required": ["Input Field"]
                                }
                            },
                            "output_structure": {
                                "type": "object",
                                "properties": {
                                    "Output Field": {
                                        "type": "string",
                                        "description": "Type and name of the output (e.g., 'List[int] result')"
                                    }
                                },
                                "required": ["Output Field"]
                            }
                        },
                        "required": ["problem_name", "function_name", "input_structure", "output_structure"]
                    }
                },
                "required": ["concept", "difficulty", "problem_title", "problem_statement", 
                           "test_cases", "tags", "structure"]
            }
        }]

        response = await self.llm.ainvoke(
            messages,
            functions=functions,
            function_call={"name": "generate_programming_problem"}
        )

        try:
            if hasattr(response, 'additional_kwargs') and 'function_call' in response.additional_kwargs:
                function_call = response.additional_kwargs['function_call']
                if function_call and 'arguments' in function_call:
                    result = json.loads(function_call['arguments'])
                    
                    # Ensure structure has all required fields
                    if 'structure' in result:
                        if 'problem_name' not in result['structure']:
                            result['structure']['problem_name'] = result['problem_title']
                        if 'input_structure' not in result['structure']:
                            result['structure']['input_structure'] = [
                                {"Input Field": "List[int] array"}
                            ]
                        if 'output_structure' not in result['structure']:
                            result['structure']['output_structure'] = {
                                "Output Field": "int result"
                            }
                        if 'function_name' not in result['structure']:
                            result['structure']['function_name'] = result['problem_title'].lower().replace(' ', '_')
                    
                    # Generate boilerplate code for both languages
                    java_boilerplate = JavaBoilerplateGenerator.convert_to_java_boilerplate(result['structure'])
                    python_boilerplate = PythonBoilerplateGenerator.convert_to_python_boilerplate(result['structure'])
                    
                    result['java_boilerplate'] = java_boilerplate
                    result['python_boilerplate'] = python_boilerplate
                    
                    return Problem(**result).model_dump()
            
            print(f"Response content: {response}")
            raise ValueError("No valid function call in response")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response}")
            raise ValueError(f"Failed to parse LLM response: {e}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Response: {response}")
            raise ValueError(f"Failed to generate problem: {str(e)}")
