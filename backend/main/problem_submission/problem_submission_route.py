from fastapi import APIRouter, HTTPException, Request
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

@router.post("/submit")
async def submit_problem(submission: ProblemSubmission):
    try:
        logger.info("=== Problem Submission Route ===")
        logger.info("1. Received submission request:")
        logger.info(f"Language ID: {submission.language_id}")
        logger.info(f"Source code length: {len(submission.source_code)}")
        logger.info(f"Problem ID: {submission.problem_id}")
        logger.info(f"Structure (raw): {submission.structure}")
        logger.info(f"Test cases count: {len(submission.test_cases)}")

        service = ProblemSubmissionService()
        result = await service.submit_code(
            language_id=int(submission.language_id),
            source_code=submission.source_code,
            problem_id=submission.problem_id,
            structure=submission.structure,
            test_cases=submission.test_cases
        )
        logger.info("2. Service result:", result)
        return result
    except Exception as e:
        logger.error(f"3. Error in submit_problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
