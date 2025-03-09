from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List
from .problem_generator_service import ProblemGeneratorService
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

class Complexity(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class ProblemRequest(BaseModel):
    concept: str
    complexity: Complexity

@router.post("/generate")
async def generate_problem(request: ProblemRequest):
    try:
        logger.info("=== Problem Generation Request ===")
        logger.info(f"Received request - concept: {request.concept}, complexity: {request.complexity}")
        
        service = ProblemGeneratorService()
        problem = await service.generate_problem(request.concept, request.complexity)
        
        logger.info(f"Successfully generated problem: {problem.get('problem_title', 'Unknown Title')}")
        return problem
    except Exception as e:
        logger.error(f"Error generating problem: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
