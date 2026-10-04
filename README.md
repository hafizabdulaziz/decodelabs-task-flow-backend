# 🚀 Decodelabs Task Flow Backend

Production-grade, fully tested, secure, and deployment-ready RESTful Task Management API built with Python (FastAPI), Async SQLAlchemy, Alembic, PostgreSQL (Neon), Argon2, JWT, and Docker.

---

## 📌 Project Overview
Decodelabs Task Flow Backend is an enterprise-ready backend application designed for robust task management. It implements clean architecture separation (API routers, services, database models, Pydantic schemas, and core security modules) with full asynchronous support.

---

## 🛠️ Tech Stack & Architecture
- **Phase 8:** Production vs Local Environment Switcher & Error Diagnostics.
- **Database & ORM:** PostgreSQL (Neon Serverless) via SQLAlchemy (Async)
- **Migrations:** Alembic (Async env setup)
- **Security:** Argon2 password hashing (via `passlib`) & JWT authentication (via `python-jose`)
- **Validation & Settings:** Pydantic v2 & Pydantic-Settings
- **Testing:** Pytest & Pytest-Asyncio (100% passing with zero warnings)
- **Code Quality:** Ruff (Linting & Formatting) & Mypy (Static Type Checking)
- **Containerization & Deployment:** Docker, Docker Compose, Vercel

---

## 🗂️ Directory Structure
```text
task-flow-backend/
├── alembic/                # Database migrations
├── app/
│   ├── api/v1/             # API Endpoints (auth, users, tasks)
│   ├── core/               # Security, JWT, dependency injection
│   ├── db/                 # Database session & base models
│   ├── models/             # SQLAlchemy ORM models (User, Task)
│   ├── schemas/            # Pydantic validation schemas
│   ├── config.py           # Application settings
│   └── main.py             # FastAPI entrypoint & middleware
├── tests/                  # Automated integration tests
├── Dockerfile              # Production container build
├── docker-compose.yml      # Local container orchestration
├── vercel.json             # Vercel deployment config
├── requirements.txt        # Pinned project dependencies
└── PLAN.md / PROGRESS.md   # Project planning and tracking
```

---

## 🚀 Getting Started

### 1. Clone & Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file based on `.env.example`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/task_flow
JWT_SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_ENV=development
```

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

---

## 🔑 Authentication & Swagger UI Guide
To test authentication and execute requests via Swagger UI (`http://127.0.0.1:8000/docs`) or API clients:
1. **Login Endpoint (`POST /api/v1/auth/login`)**: Send a clean JSON payload containing `email` and `password`.
   ```bash
   curl -X 'POST' \
     'http://127.0.0.1:8000/api/v1/auth/login' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "email": "user@example.com",
       "password": "SecurePassword123!"
     }'
   ```
2. Receive the JWT `access_token` in response.
3. Click the **Authorize** button at the top of Swagger UI (or pass `-H "Authorization: Bearer <token>"` in cURL) to authenticate protected endpoints (`/users/me`, `/tasks/`, etc.).

---

## 🧪 Testing & Code Quality Checks
- **Run Tests (Zero Warnings):**
  ```bash
  python -m pytest
  ```
- **Run Linter (Ruff):**
  ```bash
  python -m ruff check .
  ```
- **Run Type Checker (Mypy):**
  ```bash
  python -m mypy .
  ```

---

## 🐳 Docker Execution
```bash
docker-compose up --build
```
