GLOBAL PORT PASS — ONE-COMMAND LOCAL RUN

1) Copy env and set a real SECRET_KEY:
   cp .env.example .env
   # then open .env and change SECRET_KEY to a long random string

2) Start everything (API + DB + MinIO):
   docker compose up --build

3) Open:
   API docs:  http://localhost:8000/docs
   MinIO UI:  http://localhost:9001  (minioadmin / minioadmin)

4) Flow:
   - Register/Login
   - Upload documents
   - Create one-time passcodes
   - Verify passcode to get one-time download URL
