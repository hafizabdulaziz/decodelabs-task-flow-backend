# Task Flow Backend

An asynchronous RESTful task management API engineered with FastAPI, SQLAlchemy 2.0 (Async), Alembic, and PostgreSQL. Built with modular architectural patterns, Pydantic v2 type validation, JWT authentication, sliding-window rate limiting, and comprehensive automated test coverage.

---

## Technical Stack & Dependencies

- **Framework:** FastAPI `v0.115.8` running on Uvicorn ASGI server (`v0.34.0`)
- **Data Validation & Serialization:** Pydantic `v2.10.6` enforcing strict runtime DTO contracts
- **Database & ORM:** PostgreSQL (`asyncpg`) powered by SQLAlchemy `v2.0.38` (AsyncEngine) & Alembic `v1.14.1`
- **Security & Cryptography:** JWT Bearer tokens (`python-jose`) and Argon2 password hashing (`passlib`)
- **Testing Suite:** Pytest `v8.3.4`, `pytest-asyncio`, and `respx` (mock HTTP routing)
- **Code Quality & Type Checking:** Ruff `v0.9.5` (linter) and Mypy `v1.15.0` (static type checker)

---

## Architecture & Project Structure

The repository follows a clean, single-responsibility modular architecture:

```text
task-flow-backend/
├── alembic/                 # Database schema migration scripts and environment setup
├── app/
│   ├── api/v1/              # Version 1 API route controllers
│   │   ├── auth.py          # User registration, OAuth2 login, and token revocation
│   │   ├── chat.py          # AI Assistant widget command dispatcher interface
│   │   ├── external.py      # Open-Meteo third-party weather API facade proxy
│   │   ├── system.py        # Server health check and telemetry metrics endpoints
│   │   ├── tasks.py         # Task CRUD operations, filtering, pagination, and search
│   │   └── users.py         # Authenticated user profile retrieval (/users/me)
│   ├── core/                # Core enterprise infrastructure
│   │   ├── config.py        # Pydantic Settings environment configuration
│   │   ├── deps.py          # FastAPI dependency injection (DB session, current user)
│   │   ├── jwt.py           # JWT token generation and payload verification
│   │   ├── rate_limit.py    # Sliding window rate-limiting middleware
│   │   └── security.py      # Argon2 password hashing and verification utilities
│   ├── db/                  # Database configuration
│   │   ├── base.py          # Declarative base and metadata registry
│   │   └── session.py       # Asynchronous session factory (`async_sessionmaker`)
│   ├── models/              # SQLAlchemy ORM database entities
│   │   ├── task.py          # Task entity model (title, description, status, priority, owner_id)
│   │   └── user.py          # User entity model (email, hashed_password, full_name, role, is_active)
│   ├── schemas/             # Pydantic v2 data transfer objects (DTOs)
│   │   ├── error.py         # Centralized uniform error response schema
│   │   ├── external.py      # External weather response schema
│   │   ├── task.py          # Task creation, update, and response schemas
│   │   └── user.py          # User registration and token response schemas
│   ├── services/            # Business logic and external service wrappers
│   │   ├── external_service.py # Open-Meteo weather service client
│   │   └── http_client.py   # Resilient async HTTP client wrapper
│   ├── static/              # CSS stylesheet assets for control center
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
├── .env.example             # Environment variable template
├── Dockerfile               # Production container specification
├── docker-compose.yml       # Local multi-container stack (App + PostgreSQL)
└── requirements.txt         # Exact Python package dependencies
Detailed Component Breakdown
1. API Controllers (app/api/v1/)
auth.py: Manages user sign-up with email uniqueness validation, OAuth2 password login yielding signed JWT access tokens, and a logout endpoint that revokes active sessions.

tasks.py: Exposes complete CRUD endpoints for tasks tied to the authenticated user, supporting advanced query filtering (status, priority, and text search).

users.py: Provides /users/me for fetching current user profile details via JWT verification.

chat.py: Powers the embedded AI Assistant widget by interpreting and dispatching natural language commands.

external.py: Acts as a secure backend facade proxy interfacing with the Open-Meteo weather API.

system.py: Exposes system telemetry and server health monitoring endpoints.

2. Core Security & Middleware (app/core/)
security.py: Handles password encryption and verification via Argon2.

jwt.py: Encodes and decodes JSON Web Tokens using HS256 algorithm.

rate_limit.py: Implements custom sliding-window rate-limiting middleware to track request frequency and inject standard headers (X-RateLimit-*).

deps.py: Provides dependency injectors for async database sessions and active user verification.

Environment Setup & Local Execution
1. Virtual Environment & Dependencies
Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
2. Configuration (.env)
Create a .env file in the root directory based on your environment:

Code snippet
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db
SECRET_KEY=your-secure-jwt-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_PER_MINUTE=1000
(Note: For local development without PostgreSQL, SQLite async fallback sqlite+aiosqlite:///./task_flow.db is supported).

3. Database Migrations & Server Startup
Bash
# Apply Alembic database migrations
alembic upgrade head

# Start Uvicorn development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Access the interactive Control Center dashboard at http://localhost:8000/ and API Swagger documentation at http://localhost:8000/docs.

API Authentication & Usage Guide
Register User (POST /api/v1/auth/register):

JSON
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "Test User"
}
Login (POST /api/v1/auth/login): Send request with header Content-Type: application/x-www-form-urlencoded:

Plaintext
username=user@example.com&password=SecurePassword123!&grant_type=password
(Returns a JSON response containing your access_token).

Authorized Request (GET /api/v1/tasks/): Include the token in the header:

HTTP
Authorization: Bearer <YOUR_ACCESS_TOKEN>
Automated Testing & Quality Assurance
Execute the test suite and static analysis tools locally:

Bash
# Run pytest test suite
python -m pytest

# Run Ruff linter
ruff check .

# Run Mypy type checker
mypy app tests
Containerization
Run the application and PostgreSQL database in isolated containers using Docker Compose:

Bash
docker-compose up --build
