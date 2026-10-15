# Task Flow Backend

An asynchronous FastAPI backend service providing RESTful task management, JWT authentication, role-based access control (RBAC), SQLAlchemy 2.0 ORM with PostgreSQL, rate-limiting middleware, and third-party external service integration.

---

## Technical Stack

- **Framework:** FastAPI 0.115.8 (ASGI via Uvicorn)
- **Data Validation:** Pydantic v2 (strict type enforcement & serialization)
- **Database ORM:** SQLAlchemy 2.0 (Async engine with `asyncpg` and `aiosqlite`)
- **Migrations:** Alembic 1.14.1
- **Security:** `python-jose` (JWT Bearer tokens), `passlib` (Argon2 password hashing)
- **Testing:** Pytest 8.3.4, `pytest-asyncio`, and `respx` mock routing
- **Linting & Typing:** Ruff 0.9.5 and Mypy 1.15.0

---

## Project Structure

```tree
task-flow-backend/
├── alembic/                 # Database migrations
├── app/
│   ├── api/v1/              # API route controllers (auth, tasks, users, chat, external, system)
│   ├── core/                # Core utilities (config, security, jwt, rate_limit, deps)
│   ├── db/                  # Database base and async session factory
│   ├── models/              # SQLAlchemy ORM models (User, Task)
│   ├── schemas/             # Pydantic validation schemas
│   ├── services/            # Business logic and external HTTP client wrappers
│   ├── static/              # CSS assets
│   ├── templates/           # HTML dashboard and control center UI
│   └── main.py              # FastAPI application factory and middleware
├── tests/                   # Pytest test suite (auth, tasks, rbac, security, rate_limit, errors)
├── requirements.txt         # Project dependencies
├── Dockerfile               # Container build specification
└── docker-compose.yml       # Local multi-container stack (App + PostgreSQL)
```

---

## Setup & Local Execution

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (`.env`):
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db
   SECRET_KEY=your-jwt-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   RATE_LIMIT_PER_MINUTE=1000
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## API Authentication & Usage

1. **Register User (`POST /api/v1/auth/register`):**
   ```json
   {
     "email": "user@example.com",
     "password": "SecurePassword123!",
     "full_name": "Test User"
   }
   ```

2. **Authenticate & Obtain JWT (`POST /api/v1/auth/login`):**
   Send form-urlencoded parameters: `username` (email), `password`, `grant_type` (`password`).

3. **Access Protected Endpoints (`/api/v1/tasks/`):**
   Include `Authorization: Bearer <TOKEN>` in request headers.

---

## Testing & Code Quality

- **Run Tests:**
  ```bash
  python -m pytest
  ```
- **Run Linter:**
  ```bash
  ruff check .
  ```
- **Run Type Checker:**
  ```bash
  mypy app tests
  ```
