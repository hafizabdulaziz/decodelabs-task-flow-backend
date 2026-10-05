Act as a Senior Backend & Frontend Architect supervising an end-to-end automated upgrade for DecodeLabs Project 4 (Third-Party API Integration Track).

### 1. PROJECT CONTEXT & ARCHITECTURAL OBJECTIVE
We are upgrading our FastAPI application and Frontend Control Center to fulfill DecodeLabs Project 4 requirements (Industrial Training Kit). The system acts as a protective proxy (Backend Middleman / Facade Pattern) for external third-party services (e.g., Weather API / OpenMeteo).

You must implement the 4 Core Architectural Roles:
- Role 1: THE VAULT (Credential Safeguarding & Environment Isolation)
- Role 2: THE MESSENGER (Non-Blocking Asynchronous Transport with 5s Timeouts)
- Role 3: THE TRANSLATOR (Data Pruning & Schema Alignment: 100+ raw keys -> 3-5 clean client keys)
- Role 4: THE SHIELD (Resilience, Timeouts, Fault Tolerance & Fallback Mechanisms)

ADDITIONAL UI & FEATUREREQUIREMENTS:
- UI OVERHAUL & CLEANUP: Remove all cluttered, unnecessary, redundant buttons and dead features from the UI. Keep ONLY the essential functional components.
- SMART AI CHAT BOARD (ASSISTANT): Add an integrated AI Chatbot widget in the UI that helps users navigate the system, answers queries, and can programmatically invoke backend actions (e.g., create a task or user via natural language commands).

### 2. STRICT AUTONOMOUS EXECUTION RULES
- DO NOT STOP OR ASK FOR INTERMEDIATE CONFIRMATIONS. Execute Step 1 through Step 10 continuously in a single run.
- Execute atomic Git commits immediately after completing EACH individual micro-step.
- Synchronize and append progress details to `README.md` after EVERY SINGLE STEP.
- Write clean, fully-typed Python and modern clean CSS/JS. Do not break existing core logic.

---

### 3. STEP-BY-STEP GRANULAR EXECUTION PLAN

#### STEP 1: Dependencies & Configuration Vault (The Vault)
1. Add `httpx` and `respx` to `requirements.txt` and install them.
2. Update `app/core/config.py` using Pydantic BaseSettings to securely parse `EXTERNAL_API_KEY`, `EXTERNAL_API_BASE_URL`, and `EXTERNAL_API_TIMEOUT`.
3. Update `.env.example` and verify that `.env` is strictly ignored in `.gitignore`.
- **Git Commit:** `feat(vault): configure environment variables and credential isolation`
- **README Update:** Log Step 1 under "Architecture - Role 1: The Vault".

#### STEP 2: Asynchronous HTTP Transport Setup (The Messenger)
1. Create `app/services/http_client.py` with an async HTTP client wrapper around `httpx.AsyncClient`.
2. Enforce a strict 5-second request timeout policy.
3. Hook lifespan event management in `app/main.py` for clean setup and teardown.
- **Git Commit:** `feat(messenger): introduce async HTTP client with strict 5s timeout controls`
- **README Update:** Log Step 2 under "Architecture - Role 2: The Messenger".

#### STEP 3: Response Schema Definitions (The Translator - Schemas)
1. Create `app/schemas/external.py` with Pydantic models:
   - `RawExternalData`: Internal validation schema.
   - `ClientThirdPartyDataResponse`: Sanitized client payload (3-5 keys: `location`, `temperature_celsius`, `condition`, `is_rainy`, `timestamp`).
- **Git Commit:** `feat(translator): define client-facing sanitized Pydantic models`
- **README Update:** Log Step 3 under "Architecture - Role 3: The Translator (Schemas)".

#### STEP 4: Payload Translation Pipeline (The Translator - Logic)
1. Create `app/services/external_service.py` to handle third-party requests.
2. Implement transformation functions that strip 100+ raw parameters into the clean 3-5 key schema.
- **Git Commit:** `feat(translator): build data extraction and reformatting logic`
- **README Update:** Log Step 4 under "Architecture - Role 3: The Translator (Logic)".

#### STEP 5: Fault Tolerance & Shielding (The Shield)
1. Wrap all external API requests in `app/services/external_service.py` with try-except blocks for `httpx.TimeoutException` and status errors.
2. Implement fallback placeholder data generators so network timeouts or 5xx provider crashes return graceful degraded responses instead of internal 500 errors.
- **Git Commit:** `feat(shield): implement error shielding, timeouts, and fallback mechanisms`
- **README Update:** Log Step 5 under "Architecture - Role 4: The Shield".

#### STEP 6: API Facade Router & OpenAPI Integration
1. Create `app/api/v1/endpoints/external.py` exposing `GET /api/v1/external/weather`.
2. Connect endpoints to the service layer and register the router in `app/api/v1/router.py`.
- **Git Commit:** `feat(api): expose facade proxy endpoint with OpenAPI docs`
- **README Update:** Log Step 6 under "API Endpoints - Third-Party Facade".

#### STEP 7: UI Cleanup & Clutter Removal
1. Inspect the frontend HTML/JS files (`app/templates/index.html` or static files).
2. Remove all unused, non-functional, and extra clutter buttons, redundant diagnostic logs, or dead UI components.
3. Streamline layout so only core working panels remain: Auth, Tasks, Third-Party Facade Data, and System Health.
- **Git Commit:** `refactor(ui): declutter frontend interface and streamline core action panels`
- **README Update:** Log Step 7 under "Frontend Interface Streamlining".

#### STEP 8: Integrated AI Chat Board & Action Agent
1. Add an AI Chatbot widget component to the UI (collapsible floating chat window/board).
2. Implement backend endpoint `POST /api/v1/chat/assistant` (in `app/api/v1/endpoints/chat.py`) that processes user prompts.
3. Enable the AI Assistant to interpret natural language commands (e.g., "create task [title]", "register user [email]") and execute programmatic API calls on the user's behalf.
- **Git Commit:** `feat(chat): integrate AI chat assistant board with automated task/user action execution`
- **README Update:** Log Step 8 under "AI Chat Board & Automation Agent".

#### STEP 9: Automated Pytest Integration Suite
1. Create `tests/test_external_integration.py` covering:
   - External API async fetch and transformation.
   - Timeout and 5xx error fallback handling.
   - AI Chat Assistant request routing and action triggers.
2. Run `pytest` and ensure 100% pass status.
- **Git Commit:** `test(suite): add automated test coverage for facade endpoints and ai assistant`
- **README Update:** Log Step 9 under "Automated Test Suite Verification".

#### STEP 10: Final System Polish & Build Verification
1. Perform a final code cleanup, formatting, and route verification.
2. Finalize `README.md` with updated features, API endpoints, setup instructions, and testing details.
- **Git Commit:** `chore(release): finalize DecodeLabs Project 4 release with streamlined UI and AI board`
- **README Update:** Finalize main `README.md` and project documentation.

---

### 4. FINAL OUTPUT REQUIREMENT
After completing ALL 10 steps continuously, output a detailed **Final Execution Summary Report** containing:
1. List of all Git Commits (Hashes & Commit Messages).
2. Summary of UI Refactoring (items removed vs core features retained).
3. AI Chat Board capabilities overview.
4. Architecture Mapping (Vault, Messenger, Translator, Shield)[cite: 16].
5. Pytest Execution Results.