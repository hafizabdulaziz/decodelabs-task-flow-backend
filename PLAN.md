# DECODELABS TASK FLOW API - CONTROL CENTER UI ROADMAP

## Theme & Architecture
- **Color Palette:** Deep Emerald / Obsidian Amber Accent Palette (`#0B132B`, `#1C2541`, `#3A506B`, `#5BC0BE`, Accent: `#FF9F1C`).
- **UI/UX Transformation:** Split-layout Dashboard (Interactive API Console, Real-time Metrics, Token Inspector, and Live Request Logs).

---

## Phase 1: Project Re-Architecture & Base Design System Setup
- [x] **Part 1.1:** Setup modular project structure for Custom UI templates and static assets. (`feat(ui): initialize modular static and template directory structure`)
- [x] **Part 1.2:** Configure Tailwind CSS engine with custom theme colors (Deep Emerald / Obsidian Cyan). (`style(theme): add custom dark emerald color tokens and typography config`)
- [x] **Part 1.3:** Replace default Swagger UI HTML shell with a custom-rendered FastAPI endpoint `/docs`. (`feat(docs): mount custom HTML route for production API dashboard`)

## Phase 2: Modern Layout & Glassmorphism Dashboard UI
- [ ] **Part 2.1:** Build top navigation bar with live server status, environment badge, and fast-action tools. (`ui(header): implement top navigation bar with dynamic status indicator`)
- [ ] **Part 2.2:** Construct split-view dashboard sidebar (Endpoints Directory, Schemas, Analytics, Logs). (`ui(sidebar): build responsive navigation sidebar with category filtering`)
- [ ] **Part 2.3:** Apply glassmorphism styling (backdrop-blur, custom borders) to all endpoint cards. (`ui(cards): convert Swagger endpoint panels into glassmorphic cards`)

## Phase 3: Interactive Auth & Token Management Suite
- [ ] **Part 3.1:** Create sticky top-tier Quick Auth Bar for Bearer JWT Injection. (`feat(auth-ui): create dedicated JWT quick-injection status panel`)
- [ ] **Part 3.2:** Add visual Token Decoder & Inspector modal (JWT Header, Payload, Expiry counter). (`feat(token-inspector): add frontend JWT decode and expiration visualizer`)
- [ ] **Part 3.3:** Auto-persist session tokens in browser state with 1-click token clear/refresh. (`feat(session): handle token persistence and session lifecycle management`)

## Phase 4: Endpoint UI Overhaul & Interactive Console
- [ ] **Part 4.1:** Restructure Authentication Endpoints (`/register`, `/login`) with JSON Payload Builder. (`ui(auth-endpoints): redesign login and register payload test modules`)
- [ ] **Part 4.2:** Restructure User Profile Endpoints (`/users/me`) with visual response visualizer. (`ui(user-endpoints): re-skin user profile and update interfaces`)
- [ ] **Part 4.3:** Restructure Task Management Endpoints (`/tasks/`) with filter tags and priority badges. (`ui(task-endpoints): enhance task CRUD controllers with status indicators`)

## Phase 5: Real-Time API Metrics & Health Operations
- [ ] **Part 5.1:** Integrate real-time Server Uptime and Latency widget inside `/health` tab. (`feat(metrics): add real-time health and uptime execution widget`)
- [ ] **Part 5.2:** Build memory usage and active request counter visual charts. (`ui(telemetry): design visual performance indicators for API diagnostics`)
- [ ] **Part 5.3:** Connect `/metrics` route with interactive tabular data display. (`feat(prometheus): format raw metrics into human-readable dashboard widgets`)

## Phase 6: Schema Viewer & OpenAPI Spec Visualizer
- [ ] **Part 6.1:** Redesign Pydantic Schema section into interactive accordion cards with copyable JSON examples. (`ui(schemas): rebuild object schema viewer with code-highlighting`)
- [ ] **Part 6.2:** Add search and filter bar for quick schema/model lookup. (`feat(schema-search): implement fuzzy search for Pydantic response models`)

## Phase 7: Live Request / Response Console & History Log
- [ ] **Part 7.1:** Build interactive Terminal Console at bottom-dock for Curl commands and HTTP Responses. (`ui(console): design docked interactive HTTP response log terminal`)
- [ ] **Part 7.2:** Add 1-click "Copy as Curl" and "Download Response JSON" buttons. (`feat(console-tools): add request export utilities for cURL and JSON payloads`)
- [ ] **Part 7.3:** Implement request execution history storage (stores last 10 API executions). (`feat(history): retain client-side request history with quick re-run trigger`)

## Phase 8: Advanced Enterprise Features (Portfolio Elevators)
- [ ] **Part 8.1:** Add "Production vs Local Environment" switcher toggle. (`feat(env-switch): implement dynamic base-URL toggle mechanism`)
- [ ] **Part 8.2:** Add interactive Rate Limiting status bar indicator (`X-RateLimit` headers visualizer). (`ui(rate-limit): display rate limit quotas dynamically per route execution`)
- [ ] **Part 8.3:** Integrate custom API Error Diagnostic tool for 4xx/5xx responses with helpful hints. (`feat(diagnostics): build smart error diagnostic panel for API debugging`)

## Phase 9: Comprehensive Documentation & OpenAPI Tuning
- [ ] **Part 9.1:** Update OpenAPI metadata (Title, Description, Contact info, Tags) in FastAPI app definition. (`docs(openapi): update API metadata, tags, and production description`)
- [ ] **Part 9.2:** Embed custom Markdown documentation panel directly inside dashboard header. (`docs(dashboard): add embedded documentation guide for testing endpoints`)

## Phase 10: Final Audit, Build Validation & Portfolio Polish
- [ ] **Part 10.1:** Execute full Pytest automated test suite to ensure no backend breaking changes. (`test(suite): validate all authentication and task endpoints pass with 100% accuracy`)
- [ ] **Part 10.2:** Run code formatting and static code checks via Ruff. (`style(lint): format codebase and fix linting errors across modules`)
- [ ] **Part 10.3:** Update README.md with high-resolution screenshots, feature list, and architecture guide. (`docs(readme): finalize project documentation with updated UI showcase and features`)
