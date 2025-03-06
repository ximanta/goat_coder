Refer:
frontend/README.md
backend/README.md

## Developer Note

1. Create ```frontend/.env``` add the following:
```
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

2. Create ```backend/.env``` add the following:
```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT_NAME=
AZURE_OPENAI_API_VERSION=

JUDGE0_BASE_URL=
JUDGE0_RAPIDAPI_KEY=
JUDGE0_RAPIDAPI_HOST=

SULU_BASE_URL=
SULU_API_KEY=
```

- Judge0 CE RapidAPI - Sign up for Key at:
https://rapidapi.com/judge0-official/api/judge0-ce/playground/apiendpoint_489fe32c-7191-4db3-b337-77d0d3932807
- Sulu Judge0 CE - Signup for API Key at https://platform.sulu.sh/apis/judge0/judge0-ce/readme

3. To run backend: Conda Environment with Python 3.9.19 - ```uvicorn app:app --reload```
4. To run tests from backend: ```pytest tests/```
5. To run frontend: ```npm install``` and ```npm run dev```