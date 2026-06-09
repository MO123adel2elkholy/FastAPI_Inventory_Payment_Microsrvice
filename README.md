# FastAPI Inventory & Payment Microservice

Simple monorepo: FastAPI backend + React frontend.

Ports
- Backend FastAPI: http://localhost:8000 (docs: /docs)
- Frontend (nginx): http://localhost:3000
- Redis: 6379

Prerequisites
- Docker & Docker Compose (v2+)
- (optional) Node + npm for frontend development

Quick start (production-like)
1. From project root:
   docker compose up --build -d
2. View backend docs: http://localhost:8000/docs
3. View frontend: http://localhost:3000

Development (backend)
1. python -m venv .venv
2. .venv\Scripts\activate
3. pip install -r requirements.txt
4. uvicorn main:app --reload --port 8000

Development (frontend)
1. cd inventory-frontend
2. npm install
3. npm start

Environment variables
- Use a `.env` file at project root for backend settings. Example:
  REDIS_URL=redis://redis:6379/0
  # Add APP-specific secrets here

Notes
- Dockerfile expects backend entrypoint to be `main:app`. Change the CMD in Dockerfile to match your actual module path if different.
- Redis is required by the backend (redis, redis-om in requirements.txt).

Troubleshooting
- If frontend doesn't show latest code, rebuild images:
  docker compose up --build --force-recreate frontend
- View logs:
  docker compose logs -f backend
  docker compose logs -f frontend

License
- Project files: follow repo licensing.