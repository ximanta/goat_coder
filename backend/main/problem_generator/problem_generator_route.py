from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List
from .problem_generator_service import ProblemGeneratorService

router = APIRouter()

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
        service = ProblemGeneratorService()
        problem = await service.generate_problem(request.concept, request.complexity)
        return problem
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
