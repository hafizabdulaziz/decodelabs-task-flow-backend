# Task Flow Backend (`task-flow-backend`)

Production-grade, asynchronous enterprise FastAPI backend engineered with robust security, asynchronous database operations, rate limiting, external service facades, and comprehensive automated test coverage.

---

## 🚀 Technical Summary & Stack

- **Framework:** [FastAPI v0.115.8](https://fastapi.tiangolo.com/) running on [Uvicorn v0.34.0](https://www.uvicorn.org/)
- **Data Validation & Serialization:** [Pydantic v2.10.6](https://docs.pydantic.dev/) with strict type enforcement
- **Database ORM:** [SQLAlchemy v2.0.38](https://www.sqlalchemy.org/) (Async engine with `asyncpg` for PostgreSQL and `aiosqlite` for testing)
- **Migrations:** [Alembic v1.14.1](https://alembic.sqlalchemy.org/)
- **Security & Authentication:** `python-jose` (JWT Bearer tokens), `passlib` with Argon2 password hashing
- **Rate Limiting:** Sliding-window rate limiter middleware with configurable limits and standard headers (`X-RateLimit-*`)
- **Resilience & External Services:** HTTPX-based resilient HTTP client with timeout, retry, and circuit-breaker patterns interfacing with Open-Meteo weather API
- **Testing Suite:** [Pytest v8.3.4](https://docs.pytest.org/) with `pytest-asyncio` and `respx` mock routing (100% passing test suite)
- **Code Quality & Linting:** [Ruff v0.9.5](https://astral.sh/ruff) and [Mypy v1.15.0](https://mypy.readthedocs.io/)

---

## 📂 Architecture & Directory Layout

```tree
task-flow-backend/
├── alembic/                 # Database migration scripts & env configuration
│   ├── env.py
│   └── versions/            # Revision migration scripts
├── app/
│   ├── api/v1/              # Version 1 API routers
│   │   ├── auth.py          # Authentication (register, login, logout token revocation)
│   │   ├── chat.py          # AI Assistant widget controller & agentic command dispatcher
│   │   ├── external.py      # Third-party facade proxy (Open-Meteo weather integration)
│   │   ├── system.py        # System health & telemetry endpoints
│   │   ├── tasks.py         # Task CRUD, filtering, pagination & search
│   │   └── users.py         # User profile & account management (/users/me)
│   ├── core/                # Core enterprise infrastructure
│   │   ├── config.py        # Pydantic Settings environment configuration
│   │   ├── deps.py          # FastAPI dependency injection (current user, DB session)
│   │   ├── jwt.py           # JWT token generation & payload decoding
│   │   ├── rate_limit.py    # Rate limiting middleware & sliding window tracker
│   │   └── security.py      # Password hashing (Argon2) & verification utilities
│   ├── db/                  # Database session management
│   │   ├── base.py          # Declarative base & metadata registry
│   │   └── session.py       # Async session factory (`async_sessionmaker`)
│   ├── models/              # SQLAlchemy ORM database models
│   │   ├── task.py          # Task entity model (id, title, description, status, priority, owner_id)
│   │   └── user.py          # User entity model (id, email, hashed_password, full_name, is_active, role)
│   ├── schemas/             # Pydantic v2 data transfer objects (DTOs)
│   │   ├── error.py         # Standardized error response schema
│   │   ├── external.py      # External weather response schema
│   │   ├── task.py          # Task creation, update, filter & response schemas
│   │   └── user.py          # User registration, login & response schemas
│   ├── services/            # Business logic & external service integration
│   │   ├── external_service.py # Open-Meteo facade service wrapper
│   │   └── http_client.py   # Reusable async HTTP client wrapper
│   ├── static/              # Frontend static assets (CSS stylesheets)
│   ├── templates/           # Embedded Control Center dashboard & UI templates
│   │   ├── dashboard.html   # Full API Control Center dashboard
│   │   └── index.html       # Streamlined API gateway dashboard
│   └── main.py              # FastAPI application factory, middleware & exception handlers
├── tests/                   # Comprehensive Pytest test suite
│   ├── conftest.py          # Async test fixtures, test database setup & client overrides
│   ├── test_auth.py         # Authentication & token revocation tests
│   ├── test_errors.py       # Global centralized exception handling tests
│   ├── test_external_integration.py # Mocked external facade (Respx) tests
│   ├── test_rate_limit.py   # Rate limiting header & threshold tests
│   ├── test_rbac.py         # Role-Based Access Control (RBAC) tests
│   ├── test_security.py     # Password hashing & JWT security tests
│   └── test_tasks.py        # Task CRUD, filtering, search & ownership tests
├── .env.example             # Environment variable template
├── alembic.ini              # Alembic configuration
├── Dockerfile               # Production container definition
├── docker-compose.yml       # Multi-container local orchestration (App + PostgreSQL)
├── mypy.ini                 # Static type checking configuration
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Exact Python package dependencies
└── run.bat                  # Windows startup batch script
```

---

## ⚙️ Environment Setup & Configuration

1. Clone the repository and navigate to the project directory:
   ```bash
   cd task-flow-backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install exact dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (`.env`):
   Copy `.env.example` to `.env` and configure your database URL and secret keys:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db
   SECRET_KEY=your-super-secret-jwt-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   RATE_LIMIT_PER_MINUTE=1000
   ```
   *(For local testing without PostgreSQL, SQLite async fallback `sqlite+aiosqlite:///./task_flow.db` is supported).*

---

## 🗄️ Database Migrations & Local Execution

1. Run Alembic database migrations to apply latest schema revisions:
   ```bash
   alembic upgrade head
   ```

2. Start the Uvicorn ASGI development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Access the interactive API Control Center dashboard at **[http://localhost:8000/](http://localhost:8000/)** or FastAPI Swagger Docs at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 🔐 API Reference & Authentication Guide

### 1. Register User (`POST /api/v1/auth/register`)
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "Test User"
  }
  ```

### 2. Login & Obtain JWT Token (`POST /api/v1/auth/login`)
- **Content-Type:** `application/x-www-form-urlencoded`
- **Form Fields:** `username` (email), `password`, `grant_type` (`password`)
- **cURL Example:**
  ```bash
  curl -X POST "http://localhost:8000/api/v1/auth/login" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -d "username=user@example.com&password=SecurePassword123!&grant_type=password"
  ```

### 3. Authorized Task Management (`/api/v1/tasks/`)
- Include the Bearer token in the `Authorization` header for protected endpoints:
  ```bash
  curl -X GET "http://localhost:8000/api/v1/tasks/" \
       -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
  ```

---

## 🛡️ Core Technical Mechanisms

- **Centralized Error Handling:** Global exception handlers catch FastAPI `HTTPException`, SQLAlchemy errors, and unhandled exceptions, returning uniform JSON error responses (`app/schemas/error.py`).
- **Rate Limiting Middleware:** Sliding window rate limiter tracking client requests per minute, returning HTTP 429 when limits are exceeded with informative headers.
- **RBAC & Security:** Dependency injection (`app/core/deps.py`) enforces active user status, token verification, and role privileges (`role` field on `UserModel`).
- **External Facade:** Service wrapper (`app/services/external_service.py`) securely abstracts third-party weather API calls with timeout controls and shielding.

---

## 🧪 Testing & Code Quality Assurance

- **Run Pytest Test Suite:**
  ```bash
  python -m pytest -v
  ```
- **Run Ruff Linter:**
  ```bash
  ruff check .
  ```
- **Run Mypy Type Check:**
  ```bash
  mypy app tests
  ```

---

## 🐳 Containerization & Docker

1. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. The application runs on port 8000 alongside an isolated PostgreSQL container instance.
