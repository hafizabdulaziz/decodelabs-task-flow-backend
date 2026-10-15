# Task Flow Backend

An asynchronous FastAPI backend service providing RESTful task management, JWT authentication, role-based access control (RBAC), SQLAlchemy 2.0 ORM with PostgreSQL, rate-limiting middleware, and third-party external service integration.

---

## Technical Stack & Dependencies

- **Framework:** FastAPI 0.115.8 running on Uvicorn ASGI server
- **Validation & Serialization:** Pydantic v2.10.6 (strict type enforcement)
- **Database ORM:** SQLAlchemy 2.0.38 (Async engine with `asyncpg` for PostgreSQL and `aiosqlite` for testing)
- **Migrations:** Alembic 1.14.1
- **Security:** `python-jose` (JWT Bearer tokens), `passlib` with Argon2 password hashing
- **Testing:** Pytest 8.3.4, `pytest-asyncio`, and `respx` mock routing
- **Code Quality:** Ruff 0.9.5 and Mypy 1.15.0

---

## Architecture & Directory Layout

```tree
task-flow-backend/
├── alembic/                 # Database migration scripts and environment setup
├── app/
│   ├── api/v1/              # API version 1 route controllers
│   │   ├── auth.py          # User registration, login, and JWT token revocation
│   │   ├── chat.py          # AI Assistant widget command dispatcher
│   │   ├── external.py      # Open-Meteo third-party weather API facade proxy
│   │   ├── system.py        # Health check and telemetry endpoints
│   │   ├── tasks.py         # Task CRUD operations, filtering, pagination, and search
│   │   └── users.py         # Authenticated user profile retrieval (/users/me)
│   ├── core/                # Core application infrastructure
│   │   ├── config.py        # Pydantic Settings environment configuration
│   │   ├── deps.py          # FastAPI dependency injection (DB session, current user)
│   │   ├── jwt.py           # JWT token generation and verification
│   │   ├── rate_limit.py    # Sliding window rate-limiting middleware
│   │   └── security.py      # Argon2 password hashing and verification
│   ├── db/                  # Database configuration
│   │   ├── base.py          # Declarative base and metadata registry
│   │   └── session.py       # Asynchronous session factory (`async_sessionmaker`)
│   ├── models/              # SQLAlchemy ORM database entities
│   │   ├── task.py          # Task entity model (title, description, status, priority, owner_id)
│   │   └── user.py          # User entity model (email, hashed_password, full_name, role, is_active)
│   ├── schemas/             # Pydantic v2 data transfer objects (DTOs)
│   │   ├── error.py         # Centralized error response schema
│   │   ├── external.py      # Weather response schema
│   │   ├── task.py          # Task creation, update, and response schemas
│   │   └── user.py          # User registration and token response schemas
│   ├── services/            # Business logic and external service wrappers
│   │   ├── external_service.py # Open-Meteo weather service client
│   │   └── http_client.py   # Resilient async HTTP client wrapper
│   ├── static/              # CSS stylesheet assets
│   ├── templates/           # Embedded Control Center dashboard HTML interfaces
│   └── main.py              # FastAPI application factory, middleware, and exception handlers
├── tests/                   # Automated test suite
│   ├── conftest.py          # Async test fixtures and database session overrides
│   ├── test_auth.py         # Authentication and token revocation tests
│   ├── test_errors.py       # Centralized exception handling tests
│   ├── test_external_integration.py # Mocked external weather facade tests
│   ├── test_rate_limit.py   # Rate-limiting header and threshold tests
│   ├── test_rbac.py         # Role-based access control tests
│   ├── test_security.py     # Password hashing and JWT security tests
│   └── test_tasks.py        # Task CRUD, search, and filter tests
├── requirements.txt         # Project dependencies
├── Dockerfile               # Container specification
└── docker-compose.yml       # Local multi-container stack (App + PostgreSQL)
```

---

## Detailed Component Breakdown

### 1. API Controllers (`app/api/v1/`)
- **`auth.py`**: Handles user registration with email uniqueness checks, OAuth2 password login returning signed JWT access tokens, and a logout endpoint that revokes the active session token.
- **`tasks.py`**: Provides full CRUD operations for tasks associated with the authenticated user. Includes query parameter filtering (`status_filter`, `priority`, search query `q`).
- **`users.py`**: Exposes `/users/me` to retrieve the profile of the currently authenticated user based on the provided JWT Bearer token.
- **`chat.py`**: Powers the embedded AI Assistant widget by dispatching natural language commands (e.g. creating tasks or checking system status).
- **`external.py`**: Acts as a backend facade proxy wrapping the Open-Meteo weather API with input validation and response sanitization.
- **`system.py`**: Exposes health check endpoints (`/health`) returning server status and execution telemetry.

### 2. Core Security & Middleware (`app/core/`)
- **`security.py`**: Implements secure password hashing using Argon2 via Passlib, along with password verification functions.
- **`jwt.py`**: Encodes and decodes JSON Web Tokens (JWT) using HMAC-SHA256 (`HS256`).
- **`rate_limit.py`**: Implements sliding-window rate limiting middleware that tracks client request frequency and injects standard rate-limiting headers.
- **`deps.py`**: Provides FastAPI dependency functions for injecting asynchronous database sessions and validating the current active user from the authorization header.

---

## Setup & Local Execution

1. **Clone and Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (`.env`):**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db
   SECRET_KEY=your-secure-jwt-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   RATE_LIMIT_PER_MINUTE=1000
   ```
   *(For local SQLite fallback without PostgreSQL, use: `sqlite+aiosqlite:///./task_flow.db`)*

4. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start Development Server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Access the dashboard at `http://localhost:8000/` and interactive Swagger documentation at `http://localhost:8000/docs`.

---

## API Authentication & Usage Guide

1. **Register User (`POST /api/v1/auth/register`):**
   ```json
   {
     "email": "user@example.com",
     "password": "SecurePassword123!",
     "full_name": "Test User"
   }
   ```

2. **Login (`POST /api/v1/auth/login`):**
   Send request with `Content-Type: application/x-www-form-urlencoded`:
   ```text
   username=user@example.com&password=SecurePassword123!&grant_type=password
   ```
   Returns an `access_token`.

3. **Authorized Request (`GET /api/v1/tasks/`):**
   Include header: `Authorization: Bearer <access_token>`.

---

## Running Tests & Code Quality Checks

- **Run Pytest Test Suite:**
  ```bash
  python -m pytest
  ```
- **Run Ruff Linter:**
  ```bash
  ruff check .
  ```
- **Run Mypy Type Checker:**
  ```bash
  mypy app tests
  ```
