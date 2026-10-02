# TASK INSTRUCTIONS: Task-Flow Backend Refactoring, Validation Fixes & Strict Git Discipline

## OBJECTIVE
You are acting as a Senior Backend & System Security Engineer. Your goal is to systematically fix all OAuth2 authentication errors, Swagger UI integration issues, Pydantic schema validations, and end-to-end endpoint failures in the `hafizabdulaziz/decodelabs-task-flow-backend` repository.

You must execute every task in micro-steps and adhere strictly to the **Git Commit Discipline Rules** below.

---

## STRICT GIT COMMIT DISCIPLINE (NON-NEGOTIABLE)

1. **Micro-Commit Requirement:**
   - Do NOT combine multiple structural or code changes into a single commit.
   - For every single phase, you MUST make at least **5 to 6 granular Git commits**.
   - Every single micro-step (e.g., updating a schema, fixing a single endpoint handler, adding a test, modifying an error handler) MUST be followed immediately by a git commit.

2. **Commit Message Standard:**
   - Use Conventional Commits format: `<type>(<scope>): <short descriptive summary>`
   - Allowed Types: `fix`, `feat`, `refactor`, `test`, `docs`, `chore`.
   - Examples:
     - `fix(auth): update OAuth2 password request form fields and default values`
     - `refactor(schemas): update TaskCreate and TaskUpdate Pydantic models with explicit Enum defaults`
     - `test(users): add integration tests for authenticated /users/me endpoint`

3. **Verification Before Commit:**
   - Before each commit, ensure code formatting and syntax checks pass (e.g., Ruff / Pytest).
   - Never leave uncommitted changes between micro-steps.

---

## DETAILED TECHNICAL SCOPE & FIXES

### 1. OAuth2 Login & Swagger UI Form-Data Alignment
- **Issue:** `/api/v1/auth/login` fails when tested via Swagger UI due to invalid `grant_type` inputs (e.g., passing arbitrary strings instead of `password`) and missing form field definitions.
- **Actions Required:**
  - Standardize FastAPI's `OAuth2PasswordRequestForm` dependency for the login endpoint.
  - Explicitly document `grant_type="password"` as default in Swagger OpenAPI schema.
  - Ensure password field accepts valid request strings and returns clear `422 Unprocessable Entity` validation messages if regex or length rules fail.
  - **Git Commits:** Make at least 5 distinct micro-commits for form definition, route handler, schema updates, doc annotations, and login unit tests.

### 2. Authentication Context & Header Propagation
- **Issue:** Protected endpoints (`GET /api/v1/users/me`, `PATCH /api/v1/users/me`, task management endpoints) throw `401 Unauthorized` (`Not authenticated`) due to missing or improperly configured Bearer token dependencies in OpenAPI.
- **Actions Required:**
  - Verify `HTTPBearer` / `OAuth2PasswordBearer` scheme is correctly bound to all protected router dependencies.
  - Ensure Swagger UI displays the authorization lock icon on all protected routes and correctly attaches `Authorization: Bearer <token>` headers upon authorization.
  - Update current user dependency to extract, decode, and validate active JWT rotation tokens accurately.
  - **Git Commits:** Make separate micro-commits for security scheme updates, dependency fixes, user route updates, error handling for expired tokens, and auth integration tests.

### 3. Task Management Payload & Enum Validation
- **Issue:** Task creation and update endpoints return `422 Validation Error` or unexpected errors due to mismatched payload schemas (`status`, `priority`, `due_date`).
- **Actions Required:**
  - Define explicit Enums for Task Status (`pending`, `in_progress`, `completed`) and Priority (`low`, `medium`, `high`, `urgent`).
  - Add explicit Pydantic `Field` examples and descriptions to OpenAPI definitions for `TaskCreate`, `TaskUpdate`, and `TaskResponse` models.
  - Ensure datetime serialization/deserialization for `due_date` handles ISO-8601 strings cleanly.
  - **Git Commits:** Commit schema definitions, Enum updates, Task route refactoring, validator additions, and Pydantic test cases individually.

### 4. Response Schema Consistency & Error Handlers
- **Issue:** Inconsistent error responses between custom exceptions and Pydantic `422` validation errors.
- **Actions Required:**
  - Standardize error response JSON across all exception handlers (`status_code`, `code`, `detail`, `timestamp`).
  - Ensure no sensitive stack traces leak in non-debug environments.
  - **Git Commits:** Commit custom exception handler updates, schema standardization, middleware updates, and error-handling unit tests individually.

### 5. Test Suite Expansion & Phase Completion
- **Issue:** Existing test suite (8 tests) is insufficient for full edge-case coverage.
- **Actions Required:**
  - Expand Pytest test suite to cover expired tokens, invalid Enum inputs, missing Bearer headers, and user profile patch edge cases.
  - Ensure all unit and integration tests pass cleanly.
  - Update project tracking and documentation files.
  - **Git Commits:** Commit test additions for auth, test additions for task routes, test additions for error handling, final test fixes, and final roadmap documentation update separately.

---

## EXECUTION RULES
1. Proceed step-by-step through each fix.
2. Run tests/linters after every code modification.
3. Execute `git add` and `git commit` immediately after completing every micro-step.
4. Do NOT finish any single phase without at least 5-6 commit logs.




