from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .codeassist_chat_service import CodeAssistChatService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
chat_service = CodeAssistChatService()

class TestCase(BaseModel):
    input: List[Any]
    output: Any

class SubmissionResults(BaseModel):
    completed: bool
    passed: bool
    results: List[Any]

class ChatContext(BaseModel):
    userId: str
    concept: Optional[str] = None
    complexity: Optional[str] = None
    keywords: Optional[List[str]] = None
    problemTitle: Optional[str] = None
    problemDescription: Optional[str] = None
    programmingLanguage: Optional[str] = None
    currentCode: Optional[str] = None
    testCases: Optional[List[TestCase]] = None
    submissionResults: Optional[SubmissionResults] = None

class ChatRequest(BaseModel):
    message: str
    context: ChatContext

# Import the limiter instance.
# Option 1: If you moved the limiter to a separate module (e.g., rate_limiter.py):
# from main.rate_limiter import limiter
# Option 2: Import it from app state if your project structure allows it.
# For this example, we'll assume you have direct access to the limiter instance.
from slowapi.util import get_remote_address
from slowapi import Limiter
from starlette.requests import Request

# For demonstration purposes, we re-create a reference.
# In a production project, it is best to centralize the limiter instance.
from main.shared.rate_limiter import limiter

@router.post("/chat")
@limiter.limit("3/minute")  
# Need to include request in the function for ratelimiting
async def chat(request: Request, chat_request: ChatRequest):
    """
    Chat endpoint with rate limiting of 3 requests per minute
    """
    try:
        logger.info("=== Chat Request ===")
        logger.info(f"User ID: {chat_request.context.userId}")
        logger.info(f"Message: {chat_request.message}")
        
        # Get the response generator
        response_generator = chat_service.get_chat_response(
            message=chat_request.message,
            context=chat_request.context.model_dump()
        )
        
        # Return a streaming response
        return StreamingResponse(
            response_generator,
            media_type='text/event-stream',
            headers={"X-RateLimit-Limit": "3",
                    "X-RateLimit-Remaining": str(getattr(request.state, 'rate_limit_remaining', 3))}
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
