import os
import json
from typing import List, Dict, Any, Optional
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field
from ..boilerplate_generator.java_boilerplate_generator import JavaBoilerplateGenerator
from ..boilerplate_generator.python_boilerplate_generator import PythonBoilerplateGenerator
import logging
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from .prompt_manager import PromptManager
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pathlib import Path
import random

logger = logging.getLogger(__name__)

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

@dataclass
class ProblemMetadata:
    concept: str
    complexity: str
    problem_title: str
    problem_statement: str  # Store full problem statement
    timestamp: datetime

class ProblemHistoryCache:
    def __init__(self, max_size=10):
        self.history = deque(maxlen=max_size)
        self.expiry_time = timedelta(hours=24)

    def add_problem(self, concept: str, complexity: str, problem_title: str, problem_statement: str):
        self.history.append(ProblemMetadata(
            concept=concept,
            complexity=complexity,
            problem_title=problem_title,
            problem_statement=problem_statement,
            timestamp=datetime.now()
        ))
        self._cleanup_old_entries()

    def get_recent_problems(self, concept: str, complexity: str) -> list[ProblemMetadata]:
        """Return full ProblemMetadata objects instead of just titles"""
        self._cleanup_old_entries()
        return [
            p for p in self.history 
            if p.concept == concept and p.complexity == complexity
        ]

    def _cleanup_old_entries(self):
        now = datetime.now()
        self.history = deque(
            (p for p in self.history if now - p.timestamp < self.expiry_time),
            maxlen=self.history.maxlen
        )

class ProblemGeneratorService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.9,
        )
        self.problem_cache = ProblemHistoryCache()
        self.prompt_manager = PromptManager()
        self.java_generator = JavaBoilerplateGenerator()
        self.python_generator = PythonBoilerplateGenerator()

    def _create_avoid_problems_prompt(self, recent_problems: list[ProblemMetadata]) -> str:
        if not recent_problems:
            return ""
        
        # Load forbidden operations from config
        concept_path = self._normalize_name(recent_problems[0].concept)
        config_file = Path(__file__).parent / "prompts" / "concepts" / concept_path / "config.json"
        forbidden_ops = []
        
        if config_file.exists():
            with config_file.open() as f:
                config = json.load(f)
                for category in config.get("forbidden_operations", {}).values():
                    forbidden_ops.extend(category)
        
        problems_str = "\n\n".join(
            f"""Previously Generated Problem #{i+1}:
            Title: {p.problem_title}
            Statement: {p.problem_statement}
            Core Operation: {self._extract_core_operation(p.problem_title)}
            ---"""
            for i, p in enumerate(recent_problems)
        )
        
        return f"""
        IMPORTANT: You have previously generated these problems:

        {problems_str}

        ABSOLUTELY DO NOT generate problems that:
        1. Use any of these operations: {', '.join(forbidden_ops)}
        2. Are variations of arithmetic calculations
        3. Are simple counting problems
        4. Involve basic mathematical operations

        Instead, focus on:
        - String manipulation (reverse, replace, transform)
        - Pattern matching
        - Data validation
        - Array transformations
        - Logic operations
        """

    def _extract_core_operation(self, title: str) -> str:
        """Extract the core operation from a problem title"""
        title_lower = title.lower()
        
        operations = {
            "count": "counting operation",
            "find": "finding/searching operation",
            "convert": "conversion operation",
            "transform": "transformation operation",
            "check": "validation operation",
            "validate": "validation operation",
            "reverse": "reversal operation",
            "maximum": "max/min operation",
            "minimum": "max/min operation",
            "longest": "max/min operation",
            "shortest": "max/min operation"
        }
        
        for key, operation in operations.items():
            if key in title_lower:
                return operation
                
        return "unknown operation"

    def _get_beginner_problem_suggestions(self) -> str:
        return """
        For Basic Programming beginners, choose from these problem types:
        1. String Manipulation
           - Reverse a string
           - Count specific characters
           - Convert case (upper/lower)
           - Find longest word in a sentence
           
        2. Simple Array Operations
           - Find maximum/minimum
           - Count elements matching condition
           - Find first/last occurrence
           - Check if element exists
           
        3. Number Patterns
           - Check even/odd patterns
           - Count digits
           - Check number properties (palindrome, perfect number)
           - Convert number to digits array
           
        4. Basic Logic
           - Temperature conversion
           - Time conversion
           - Distance conversion
           - Simple scoring systems
           
        5. Character Patterns
           - Check vowels/consonants
           - Convert letter to position
           - Simple character patterns
           - Basic input validation

        IMPORTANT: For each category, create unique variations and real-world contexts.
        Example contexts:
        - Gaming scores
        - Social media posts
        - School grades
        - Sports statistics
        - Weather data
        - Shopping calculations
        - Music playlist management
        - Text message analysis
        """

    async def generate_problem(self, concept: str, complexity: str) -> Dict:
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # Add some randomness to the seed on each attempt
                random.seed(os.urandom(8))
                
                # Get recent problems to avoid
                recent_problems = self.problem_cache.get_recent_problems(concept, complexity)
                avoid_prompt = self._create_avoid_problems_prompt(recent_problems)
                
                # Get concept and complexity specific prompts
                concept_prompt = self.prompt_manager.get_concept_prompt(concept)
                complexity_prompt = self.prompt_manager.get_complexity_prompt(complexity) or ""
                context_prompt = self.prompt_manager.get_context_prompt(concept, complexity) or ""
                
                # Log the selected problem type (safely)
                if concept_prompt:
                    logger.info(f"Attempt {attempt + 1}: Using concept prompt: {concept_prompt[:200]}...")
                
                # Combine prompts
                combined_prompt = f"""
                {avoid_prompt}

                {concept_prompt}

                {complexity_prompt}

                {context_prompt}
                """

                messages = [
                    {
                        "role": "system",
                        "content": combined_prompt.strip()
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
                                "description": "Programming concepts and subconcepts used in this problem. Should include the main category and specific operations used.",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        # Main categories
                                        "arrays", "strings", "numbers", "control_flow", "data_types",
                                        # Operations
                                        "array_iteration", "array_manipulation", "string_formatting",
                                        "string_manipulation", "arithmetic", "type_conversion",
                                        "conditional_logic", "loops", "input_validation",
                                        # Data structures
                                        "lists", "arrays", "strings",
                                        # Common patterns
                                        "searching", "counting", "transformation", "validation"
                                    ]
                                },
                                "example": ["arrays", "array_iteration", "counting"]
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

                logger.info("Sending request to LLM")
                response = await self.llm.ainvoke(
                    messages,
                    functions=functions,
                    function_call={"name": "generate_programming_problem"}
                )
                logger.info("Received response from LLM")
                logger.info("Raw LLM Response:")
                logger.info(json.dumps(response.additional_kwargs, indent=2))

                try:
                    if hasattr(response, 'additional_kwargs') and 'function_call' in response.additional_kwargs:
                        function_call = response.additional_kwargs['function_call']
                        if function_call and 'arguments' in function_call:
                            result = json.loads(function_call['arguments'])
                            
                            # Fix float values in test cases if needed
                            input_types = [
                                field['Input Field'].split()[0] 
                                for field in result['structure']['input_structure']
                            ]
                            output_type = result['structure']['output_structure']['Output Field'].split()[0]
                            
                            # Add logging before fixing float values
                            logger.info("Original test cases before fixing floats:")
                            logger.info(json.dumps(result['test_cases'], indent=2))
                            
                            # Use the new fix_float_values method and ensure it's properly formatted
                            fixed_test_cases = JavaBoilerplateGenerator.fix_float_values(
                                result['test_cases'],
                                input_types,
                                output_type
                            )
                            
                            # Add logging after fixing float values
                            logger.info("Fixed test cases:")
                            logger.info(json.dumps(fixed_test_cases, indent=2))
                            
                            # Update the test cases in the result
                            result['test_cases'] = [
                                TestCase(input=test_case['input'], output=test_case['output']).model_dump()
                                for test_case in fixed_test_cases
                            ]
                            
                            # Log the final complete response
                            logger.info("Complete response being sent to client:")
                            logger.info(json.dumps(result, indent=2))

                            # Ensure the concept matches the input concept exactly
                            result['concept'] = concept
                            
                            # Store full problem details
                            self.problem_cache.add_problem(
                                concept=concept,
                                complexity=complexity,
                                problem_title=result['problem_title'],
                                problem_statement=result['problem_statement']
                            )
                            
                            logger.info(f"Successfully parsed problem: {result.get('problem_title', 'Unknown Title')}")
                            
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
                            java_boilerplate = self.java_generator.convert_to_java_boilerplate(result['structure'])
                            python_boilerplate = self.python_generator.convert_to_python_boilerplate(result['structure'])
                            
                            result['java_boilerplate'] = java_boilerplate
                            result['python_boilerplate'] = python_boilerplate
                            
                            final_response = Problem(**result).model_dump()
                            logger.info("Final response after model conversion:")
                            logger.info(json.dumps(final_response, indent=2))
                            
                            return final_response
                    
                    logger.error(f"Invalid response format: {response}")
                    raise ValueError("No valid function call in response")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}", exc_info=True)
                    logger.error(f"Response content: {response}")
                    raise ValueError(f"Failed to parse LLM response: {e}")
                    
                except Exception as e:
                    logger.error(f"Error generating problem: {str(e)}", exc_info=True)
                    logger.error(f"Response: {response}")
                    raise ValueError(f"Failed to generate problem: {str(e)}")

                logger.info(f"Generated problem was too similar, attempt {attempt + 1}/{max_attempts}")

            except Exception as e:
                logger.error(f"Error generating problem: {str(e)}", exc_info=True)
                logger.error(f"Response: {response}")
                raise ValueError(f"Failed to generate problem: {str(e)}")

        # If we couldn't generate a unique problem after max attempts
        logger.warning("Could not generate sufficiently different problem")
        # Return the last generated problem anyway
        return Problem(**result).model_dump()
