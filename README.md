# 🚀 Decodelabs Task Flow Backend

Production-grade, fully tested, secure, and deployment-ready RESTful Task Management API built with Python (FastAPI), Async SQLAlchemy, Alembic, PostgreSQL (Neon), Argon2, JWT, and Docker.

---

## 📌 Project Overview
Decodelabs Task Flow Backend is an enterprise-ready backend application designed for robust task management. It implements clean architecture separation (API routers, services, database models, Pydantic schemas, and core security modules) with full asynchronous support.

---

## 🛠️ Tech Stack & Architecture
- **Phase 10 (Completed):** Final Audit, Build Validation & Portfolio Polish.
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

## 🚨 Standardized Global Exception Handling & Error Schemas
Sentinel Auth Vault implements a strict, centralized global exception handling mechanism catching `HTTPException`, `RequestValidationError`, and unhandled system errors (`Exception`). All API error responses conform to a uniform Pydantic schema:

| Field | Type | Description |
| :--- | :--- | :--- |
| `error_code` | `str` | Machine-readable error code (e.g., `UNAUTHORIZED`, `VALIDATION_ERROR`, `BAD_REQUEST`, `FORBIDDEN_ACCESS`, `NOT_FOUND`, `INTERNAL_SERVER_ERROR`) |
| `message` | `str` | Human-readable explanation of the error |
| `timestamp` | `str` | ISO-8601 UTC timestamp of error occurrence |

### Example Error Response (`401 Unauthorized`)
```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Could not validate credentials",
  "timestamp": "2026-10-10T14:30:00.000000+00:00"
}
```

---

## ⚡ Rate Limiting Policy & Redis Storage Mechanics
To protect against brute-force attacks and abuse, Sentinel Auth Vault enforces strict rate limiting via high-performance sliding window tracking:
- **Authentication Routes (`/api/v1/auth/*`)**: Strictly limited to **5 requests per minute** per client IP.
- **Resource / Standard Routes**: Limited to **60 requests per minute** per client IP.

### Response Rate Limit Headers
Every response includes rate limit telemetry headers:
- `X-RateLimit-Limit`: Maximum allowed requests within the current window.
- `X-RateLimit-Remaining`: Remaining request quota in the current window.
- `Retry-After`: Seconds to wait before retrying (included only upon 429 response).

### Rate Limit Exceeded Response (`429 Too Many Requests`)
```json
{
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Maximum 5 requests per minute allowed. Retry after 58 seconds.",
  "timestamp": "2026-10-10T14:32:10.000000+00:00"
}
```

---

## 📚 API Specification & Documentation
Sentinel Auth Vault provides rich, production-grade OpenAPI spec coverage across all routes (`/docs` and `/redoc`), adhering strictly to RESTful conventions and standardized Pydantic error payloads.

### API Routes & Status Codes Summary
| Endpoint | Method | Status Codes | Description |
| :--- | :--- | :--- | :--- |
| `/api/v1/auth/register` | `POST` | `201`, `400`, `422`, `500` | Register a new user account |
| `/api/v1/auth/login` | `POST` | `200`, `401`, `422`, `500` | Authenticate user & issue JWT Bearer token |
| `/api/v1/auth/logout` | `POST` | `200`, `401`, `500` | Revoke active session / logout |
| `/api/v1/users/me` | `GET` | `200`, `401`, `404`, `500` | Fetch current authenticated user profile |
| `/api/v1/users/me` | `PATCH` | `200`, `401`, `422`, `500` | Update current user profile properties |
| `/api/v1/tasks/` | `POST` | `201`, `401`, `422`, `500` | Create a new task |
| `/api/v1/tasks/` | `GET` | `200`, `401`, `422`, `500` | List tasks with filtering, search & sorting |
| `/api/v1/tasks/{id}` | `GET` | `200`, `401`, `404`, `500` | Fetch single task by ID |
| `/api/v1/tasks/{id}` | `PATCH` | `200`, `401`, `404`, `422`, `500` | Update task by ID |
| `/api/v1/tasks/{id}` | `DELETE` | `204`, `401`, `404`, `500` | Delete task by ID |
| `/api/v1/external/weather` | `GET` | `200`, `422`, `500` | Third-party weather integration facade |
| `/api/v1/chat/assistant` | `POST` | `200`, `422`, `500` | AI Chat Assistant natural language executor |
| `/api/v1/system/status` | `GET` | `200`, `500` | System metrics & health telemetry |

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
