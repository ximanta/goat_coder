from fastapi import APIRouter, HTTPException, Request, Body
from pydantic import BaseModel
from typing import Optional, List, Any
from .problem_submission_service import ProblemSubmissionService
from ..submission_generator.java_submission_generator import JavaSubmissionGenerator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class TestCase(BaseModel):
    input: List[Any]
    output: Any

class ProblemSubmission(BaseModel):
    language_id: str
    source_code: str
    problem_id: str
    structure: str  # This should be a string containing JSON
    test_cases: list

    class Config:
        json_schema_extra = {
            "example": {
                "language_id": "4",
                "source_code": "public int solution(int[] nums) { return 0; }",
                "problem_id": "123",
                "structure": '{"function_name": "solution", "input_structure": [{"Input_Field": "int[] nums"}], "output_structure": {"Output_Field": "int result"}}',
                "test_cases": []
            }
        }

# Add new model for submissions status request
class SubmissionsStatusRequest(BaseModel):
    tokens: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "tokens": ["token1", "token2", "token3"]
            }
        }

@router.post("/submit")
async def submit_problem(
    language_id: int = Body(...),
    source_code: str = Body(...),
    problem_id: str = Body(...),
    structure: str = Body(...),
    test_cases: list = Body(...)
):
    """
    Submit code for evaluation
    """
    try:
        logger.info("=== Problem Submission Route ===")
        logger.info("1. Received submission request:")
        logger.info(f"Language ID: {language_id}")
        logger.info(f"Source code length: {len(source_code)}")
        logger.info(f"Problem ID: {problem_id}")
        logger.info(f"Structure (raw): {structure}")
        logger.info(f"Test cases count: {len(test_cases)}")
        
        service = ProblemSubmissionService()
        result = await service.submit_code(language_id, source_code, problem_id, structure, test_cases)
        
        # Fix the logging format
        logger.info("2. Service result: %s", result)  # Changed from logger.info("2. Service result:", result)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in submit_problem: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/submission-callback")
async def submission_callback(request: Request):
    try:
        # Get the raw JSON data from the request
        callback_data = await request.json()
        
        # Log the received data
        logger.info("Received Judge0 callback data:")
        logger.info(callback_data)
        
        return {"status": "success", "message": "Callback received", "data": callback_data}
    except Exception as e:
        logger.error(f"Error processing callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/submission/{submission_id}")
async def get_submission(submission_id: str):
    try:
        logger.info(f"Getting submission details for ID: {submission_id}")
        
        service = ProblemSubmissionService()
        result = await service.get_submission(submission_id)
        return result
    except Exception as e:
        logger.error(f"Error in get_submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submissions-status")
async def get_submissions_status(request: SubmissionsStatusRequest):
    """
    Get status for multiple submissions
    """
    try:
        logger.info(f"=== Getting Status for {len(request.tokens)} Submissions ===")
        logger.info(f"Tokens: {request.tokens}")
        
        service = ProblemSubmissionService()
        result = await service.get_submissions_status(request.tokens)
        
        logger.info("Batch status result:")
        logger.info(f"Completed: {result['completed']}")
        logger.info(f"All Passed: {result['passed']}")
        logger.info(f"Results count: {len(result['results'])}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting submissions status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get submissions status: {str(e)}"
        )
