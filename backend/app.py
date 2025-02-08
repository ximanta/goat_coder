import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main.problem_generator.problem_generator_route import router as problem_generator_router
from main.problem_submission.problem_submission_route import router as problem_submission_router


load_dotenv()


app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=10000000, backupCount=5),
        logging.StreamHandler(),
    ],
)

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
    ],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure routes
app.include_router(problem_generator_router, prefix="/problem-generator", tags=["problem-generator"])
app.include_router(problem_submission_router, prefix="/problem-submission", tags=["problem-submission"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
