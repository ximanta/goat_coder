import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # Make sure to import JSONResponse
from main.problem_generator.problem_generator_route import router as problem_generator_router
from main.problem_submission.problem_submission_route import router as problem_submission_router
from main.codeassist_chat.codeassist_chat_router import router as codeassist_chat_router

# Import SlowAPI components
# from slowapi import Limiter
from main.shared.rate_limiter import limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

load_dotenv()

app = FastAPI()
app.state.limiter = limiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=10000000, backupCount=5),
        logging.StreamHandler(),
    ],
)

# Add rate limit middleware - this must be added before CORS middleware
app.add_middleware(SlowAPIMiddleware)

# Register a custom exception handler for RateLimitExceeded.
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": "I'm overwhelmed with your queries. Let me cool down with a cofee - I'll be back in a minute.",
            "limit": getattr(exc, "_limit", "3/minute")
        },
        headers={"Retry-After": "60"}  # Fixed 60 seconds for 3/minute limit
    )

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure routes
app.include_router(problem_generator_router, prefix="/problem-generator", tags=["problem-generator"])
app.include_router(problem_submission_router, prefix="/problem-submission", tags=["problem-submission"])
app.include_router(codeassist_chat_router, prefix="/codeassist", tags=["codeassist"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
