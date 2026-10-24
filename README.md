# Task Flow Backend

An asynchronous RESTful task management API engineered with FastAPI, SQLAlchemy 2.0 (Async), Alembic, and PostgreSQL. Built with modular architectural patterns, Pydantic v2 type validation, JWT authentication, sliding-window rate limiting, and comprehensive automated test coverage.

## Overview

Task Flow Backend provides a centralized task management platform featuring user authentication, role-aware data isolation, task CRUD operations with advanced querying, external API integration, telemetry endpoints, and an embedded control center interface.

## Architecture & Project Structure

The project follows a modular, single-responsibility architectural layout:

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
│   ├── core/                # Infrastructure, configuration, and security
│   │   ├── config.py        # Pydantic Settings environment configuration
│   │   ├── deps.py          # FastAPI dependency injection (DB session, current user)
│   │   ├── jwt.py           # JWT token generation and payload verification
│   │   ├── rate_limit.py    # Sliding window rate-limiting middleware
│   │   └── security.py      # Argon2 password hashing and verification utilities
│   ├── db/                  # Database connectivity and session lifecycle
│   │   ├── base.py          # Declarative base and metadata registry
│   │   └── session.py       # Asynchronous session factory (async_sessionmaker)
│   ├── models/              # SQLAlchemy ORM database entities
│   │   ├── task.py          # Task entity model (title, description, status, priority, owner_id)
│   │   └── user.py          # User entity model (email, hashed_password, full_name, role, is_active)
│   ├── schemas/             # Pydantic v2 data transfer objects (DTOs)
│   │   ├── error.py         # Centralized uniform error response schema
│   │   ├── external.py      # External weather response schema
│   │   ├── task.py          # Task creation, update, and response schemas
│   │   └── user.py          # User registration and token response schemas
│   ├── services/            # Business logic and external service integrations
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
├── Dockerfile               # Container build definition
├── docker-compose.yml       # Local multi-container stack (App + PostgreSQL)
└── requirements.txt         # Pinned Python package dependencies
```

## Detailed Component Breakdown

### 1. API Controllers (`app/api/v1/`)
- **`auth.py`**: Handles user sign-up with email uniqueness validation, OAuth2 password login yielding signed JWT access tokens, and a logout endpoint that revokes active sessions.
- **`tasks.py`**: Exposes complete CRUD endpoints for tasks scoped to the authenticated user, supporting status filtering, priority levels, and text search.
- **`users.py`**: Provides `/users/me` endpoint for retrieving authenticated user profile details via JWT verification.
- **`chat.py`**: Drives the embedded AI Assistant widget by interpreting and dispatching natural language commands.
- **`external.py`**: Serves as a backend proxy facade interfacing with the Open-Meteo weather API.
- **`system.py`**: Exposes system telemetry and server health monitoring endpoints.

### 2. Core Security & Middleware (`app/core/`)
- **`security.py`**: Encrypts and verifies passwords using Argon2.
- **`jwt.py`**: Encodes and decodes JSON Web Tokens using the HS256 algorithm.
- **`rate_limit.py`**: Implements custom sliding-window rate-limiting middleware that inspects request velocity and attaches `X-RateLimit-*` headers.
- **`deps.py`**: Provides FastAPI dependency injectors for asynchronous database sessions and user authorization checks.

## Technology Stack

- **Framework**: FastAPI `v0.115.8` on Uvicorn ASGI server `v0.34.0`
- **Validation & Serialization**: Pydantic `v2.10.6` enforcing strict DTO contracts
- **Database & Migrations**: PostgreSQL (`asyncpg`) with SQLAlchemy `v2.0.38` (AsyncEngine) and Alembic `v1.14.1`
- **Security & Cryptography**: JWT Bearer tokens (`python-jose`) and Argon2 password hashing (`passlib`)
- **Testing & Verification**: Pytest `v8.3.4`, `pytest-asyncio`, and `respx` (HTTP request mocking)
- **Code Quality**: Ruff `v0.9.5` (linter) and Mypy `v1.15.0` (static type analysis)

## Environment Setup & Local Execution

### 1. Virtual Environment & Dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root directory configured for your environment:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_flow_db
SECRET_KEY=your-secure-jwt-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_PER_MINUTE=1000
```

> **Note**: For local development without a running PostgreSQL instance, SQLite async fallback (`sqlite+aiosqlite:///./task_flow.db`) is supported.

### 3. Database Migrations & Server Startup

Apply migrations and start the application server:

```bash
# Apply schema migrations via Alembic
alembic upgrade head

# Launch Uvicorn development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Control Center Dashboard: `http://localhost:8000/`
- Interactive OpenAPI Documentation: `http://localhost:8000/docs`

## API Authentication & Usage Guide

### User Registration
`POST /api/v1/auth/register`

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "Test User"
}
```

### User Login
`POST /api/v1/auth/login` (Content-Type: `application/x-www-form-urlencoded`)

```text
username=user@example.com&password=SecurePassword123!&grant_type=password
```

Response returns a JSON payload containing the `access_token`.

### Authenticated Request
Include the bearer token in the `Authorization` header for protected endpoints (e.g., `GET /api/v1/tasks/`):

```http
Authorization: Bearer <YOUR_ACCESS_TOKEN>
```

## Automated Testing & Quality Assurance

Run the automated test suite and code quality tooling:

```bash
# Execute test suite
python -m pytest

# Run linter
ruff check .

# Run static type checker
mypy app tests
```

## Containerization

Deploy the application and PostgreSQL database in isolated containers using Docker Compose:

```bash
docker-compose up --build
```
