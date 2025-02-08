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
        try:
            parsed_structure = json.loads(structure) if isinstance(structure, str) else structure
            
            # Generate complete Java submission
            java_generator = JavaSubmissionGenerator()
            complete_source = java_generator.generate_submission(source_code, parsed_structure)
            encoded_source = self.encode_base64(complete_source)
            
            # Prepare submissions for all test cases
            submissions = []
            logger.info(f"Processing {len(test_cases)} test cases")
            
            for i, test_case in enumerate(test_cases):
                input_str = self.format_input_for_java(test_case['input'])
                output_str = str(test_case['output'])
                
                logger.info(f"Test Case {i + 1}:")
                logger.info(f"Input: {input_str}")
                logger.info(f"Expected Output: {output_str}")
                
                submissions.append({
                    "language_id": language_id,
                    "source_code": encoded_source,
                    "stdin": self.encode_base64(input_str),
                    "expected_output": self.encode_base64(output_str),
                    "callback_url": os.getenv("JUDGE0_CALLBACK_URL")
                })
            
            # Submit batch request
            url = f"{self.judge0_base_url}/submissions/batch"
            payload = {"submissions": submissions}
            
            response = await self._make_request(url, payload)
            return response
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

    async def get_submissions_status(self, tokens: list[str]):
        """Get status for multiple submissions"""
        results = []
        
        for i, token in enumerate(tokens):
            try:
                result = await self.get_submission(token)
                results.append({
                    "test_case_index": i,
                    "token": token,
                    "status": result["status"],
                    "compile_output": result.get("compile_output"),
                    "stdout": result.get("stdout"),
                    "stderr": result.get("stderr"),
                    "expected_output": result.get("expected_output"),
                    "passed": result["status"]["id"] == 3  # 3 is Accepted
                })
            except Exception as e:
                logger.error(f"Error getting status for submission {token}: {e}")
                results.append({
                    "test_case_index": i,
                    "token": token,
                    "error": str(e),
                    "passed": False
                })
        
        # Calculate overall status
        all_completed = all(r.get("status", {}).get("id") not in [1, 2] for r in results)
        all_passed = all(r.get("passed", False) for r in results)
        
        return {
            "completed": all_completed,
            "passed": all_passed,
            "results": results
        }

    async def _make_request(self, url: str, payload: dict) -> dict:
        """
        Make a request to Judge0 API
        """
        try:
            logger.info(f"Making request to: {url}")
            logger.info(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                params={"base64_encoded": "true", "fields": "*"}
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            if not response.ok:
                error_text = response.text
                logger.error(f"Request failed with status {response.status_code}: {error_text}")
                raise Exception(f"Judge0 API request failed: {error_text}")
            
            result = response.json()
            logger.info(f"Response: {json.dumps(result, indent=2)}")
            
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
            raise Exception(f"Failed to make Judge0 API request: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Unexpected error in Judge0 API request: {str(e)}")
