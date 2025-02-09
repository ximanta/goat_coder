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

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        logger.info("=== Chat Request ===")
        logger.info(f"User ID: {request.context.userId}")
        logger.info(f"Message: {request.message}")
        
        # Return a streaming response
        return StreamingResponse(
            chat_service.get_chat_response(
                message=request.message,
                context=request.context.model_dump()
            ),
            media_type='text/event-stream'
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
