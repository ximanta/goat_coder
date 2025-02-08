import os
import requests
import base64
import json
import logging
from dotenv import load_dotenv
from ..submission_generator.java_submission_generator import JavaSubmissionGenerator

load_dotenv()
logger = logging.getLogger(__name__)

class ProblemSubmissionService:
    def __init__(self):
        self.judge0_base_url = os.getenv("JUDGE0_BASE_URL")
        if not self.judge0_base_url:
            raise ValueError("JUDGE0_BASE_URL environment variable is not set")

        rapidapi_key = os.getenv("JUDGE0_RAPIDAPI_KEY")
        if not rapidapi_key:
            raise ValueError("JUDGE0_RAPIDAPI_KEY environment variable is not set")

        rapidapi_host = os.getenv("JUDGE0_RAPIDAPI_HOST")
        if not rapidapi_host:
            raise ValueError("JUDGE0_RAPIDAPI_HOST environment variable is not set")

        self.headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": rapidapi_host,
            "Content-Type": "application/json"
        }

        logger.info("ProblemSubmissionService initialized with:")
        logger.info(f"Judge0 Base URL: {self.judge0_base_url}")
        logger.info(f"RapidAPI Host: {rapidapi_host}")

    def encode_base64(self, text: str) -> str:
        """Convert string to base64"""
        return base64.b64encode(str(text).encode()).decode()

    def format_input_for_java(self, input_data: list) -> str:
        """Format input data for Java program stdin"""
        # For arrays, join elements with spaces
        formatted_inputs = []
        for item in input_data:
            if isinstance(item, list):
                # Join array elements with spaces for Java input
                formatted_inputs.append(" ".join(str(x) for x in item))
            else:
                formatted_inputs.append(str(item))
        
        # Join different inputs with newlines
        return "\n".join(formatted_inputs)

    async def submit_code(self, language_id: int, source_code: str, problem_id: str, structure: str, test_cases: list):
        logger.info("=== Problem Submission Service ===")
        logger.info(f"1. Received structure (type: {type(structure)}): {structure}")
        
        try:
            parsed_structure = json.loads(structure) if isinstance(structure, str) else structure
            logger.info(f"2. Parsed structure: {parsed_structure}")
            
            # Generate complete Java submission
            java_generator = JavaSubmissionGenerator()
            logger.info("3. Creating Java generator")
            
            complete_source = java_generator.generate_submission(source_code, parsed_structure)
            
            url = f"{self.judge0_base_url}/submissions/batch"
            
            # Use the first test case for initial submission
            first_test = test_cases[0]
            logger.info(f"Using test case: {first_test}")
            
            # Format input properly for Java
            input_str = self.format_input_for_java(first_test['input'])
            output_str = str(first_test['output'])
            
            logger.info("=== Input/Output Processing ===")
            logger.info(f"Raw input: {first_test['input']}")
            logger.info(f"Formatted input string: {input_str}")
            logger.info(f"Raw output: {first_test['output']}")
            logger.info(f"Formatted output string: {output_str}")

            # Encode the inputs in base64
            encoded_source = self.encode_base64(complete_source)
            encoded_stdin = self.encode_base64(input_str)
            encoded_expected = self.encode_base64(output_str)
            
            logger.info("=== Base64 Encoded Data ===")
            logger.info(f"Encoded stdin (base64): {encoded_stdin}")
            logger.info("Decoded stdin (for verification):")
            logger.info(base64.b64decode(encoded_stdin).decode('utf-8'))

            # Payload for batch submission
            payload = {
                "submissions": [
                    {
                        "language_id": language_id,
                        "source_code": encoded_source,
                        "stdin": encoded_stdin,
                        "expected_output": encoded_expected,
                        "callback_url": os.getenv("JUDGE0_CALLBACK_URL", "http://localhost:8000/problem-submission/submission-callback")
                    }
                ]
            }
            
            querystring = {"base64_encoded":"true","wait":"false","fields":"*"}
            
            # Log request details
            logger.info("Sending request to Judge0:")
            logger.info(f"URL: {url}")
            logger.info(f"Payload: {payload}")
            
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    params=querystring
                )
                
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response body: {response.text}")
                
                response.raise_for_status()
                response_json = response.json()
                logger.info(f"Parsed response: {response_json}")
                return response_json
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                logger.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response content'}")
                raise Exception(f"Failed to submit code: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"5. Failed to parse structure JSON: {e}")
            raise Exception(f"Invalid structure format: {e}")
        except Exception as e:
            logger.error(f"5. Failed to generate Java submission: {str(e)}")
            raise Exception(f"Failed to generate Java submission: {str(e)}")

    async def get_submission(self, submission_id: str):
        """
        Get submission details from Judge0 and decode the response.
        """
        logger.info(f"=== Polling Submission {submission_id} ===")
        url = f"{self.judge0_base_url}/submissions/{submission_id}"
        
        querystring = {
            "base64_encoded": "true",
            "fields": "*"
        }
        
        # Remove Content-Type header for GET request
        headers = {
            "x-rapidapi-key": self.headers["x-rapidapi-key"],
            "x-rapidapi-host": self.headers["x-rapidapi-host"]
        }
        
        logger.info(f"Getting submission details from Judge0:")
        logger.info(f"URL: {url}")
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=querystring
            )
            
            logger.info(f"Response status: {response.status_code}")
            response_json = response.json()
            
            # Decode base64 fields
            if response_json.get("source_code"):
                response_json["source_code"] = base64.b64decode(response_json["source_code"]).decode('utf-8')
            if response_json.get("stdin"):
                response_json["stdin"] = base64.b64decode(response_json["stdin"]).decode('utf-8')
            if response_json.get("stdout"):
                response_json["stdout"] = base64.b64decode(response_json["stdout"]).decode('utf-8')
            if response_json.get("stderr"):
                response_json["stderr"] = base64.b64decode(response_json["stderr"]).decode('utf-8')
            if response_json.get("compile_output"):
                response_json["compile_output"] = base64.b64decode(response_json["compile_output"]).decode('utf-8')
            if response_json.get("message"):
                response_json["message"] = base64.b64decode(response_json["message"]).decode('utf-8')
            if response_json.get("expected_output"):
                response_json["expected_output"] = base64.b64decode(response_json["expected_output"]).decode('utf-8')

            # Log decoded response
            logger.info("Decoded Judge0 response:")
            logger.info(f"Status: {response_json.get('status', {}).get('description', 'Unknown')}")
            logger.info(f"Compile Output: {response_json.get('compile_output', 'None')}")
            logger.info(f"Stdout: {response_json.get('stdout', 'None')}")
            logger.info(f"Stderr: {response_json.get('stderr', 'None')}")
            logger.info(f"Exit Code: {response_json.get('exit_code', 'None')}")
            logger.info(f"Time: {response_json.get('time', 'None')}")
            logger.info(f"Memory: {response_json.get('memory', 'None')}")

            # Format response for frontend
            formatted_response = {
                "status": response_json.get("status", {}),
                "compile_output": response_json.get("compile_output"),
                "stdout": response_json.get("stdout"),
                "stderr": response_json.get("stderr"),
                "time": response_json.get("time"),
                "memory": response_json.get("memory"),
                "exit_code": response_json.get("exit_code"),
                "expected_output": response_json.get("expected_output")
            }

            return formatted_response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            logger.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response content'}")
            raise Exception(f"Failed to get submission: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing submission response: {str(e)}")
            raise Exception(f"Failed to process submission response: {str(e)}")
