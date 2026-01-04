# 🚀 One-Time Secure File/Text Sharing App
> **30-Day Build Challenge**

![Status](https://img.shields.io/badge/Status-Planning-blue?style=flat-square)
![Language](https://img.shields.io/badge/Language-Python-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧐 The Problem
> *Sharing sensitive information (API keys, passwords, configuration files) via email, Discord, or WhatsApp is insecure. Third-party services like Pastebin or WeTransfer store your data on their servers, creating a privacy risk.*

## 💡 The Solution
**Build a lightweight, containerized Python web application** that allows you to:
1. Upload a file or text snippet.
2. Generate a unique, secure link.
3. **Permanently delete** the data from the server immediately after it is viewed once (or after a short timer expires).

---


## Project Overview
**Goal**: Build a secure, one-time file sharing application within 30 days.
**Timeline**: December 24, 2025 → January 24, 2026
**Tech Stack**:
- **Backend**: Python / Flask
- **Storage**: Dockerized Redis (Ephemeral storage)
- **Containerization**: Docker
- **UI**: Bootstrap
- **CI/CD**: GitHub Actions

---

## 📅 Day 0: Inception & Foundation (Dec 24, 2025)
**Status**: ✅ Completed

### Report
- **Project Initiation**: Defined the core problem (secure, temporary file sharing) and the solution (OneTimeShare).
- **Public Announcement**: Launched the #OneTimeShare30 challenge on social media along with the GitHub repository.
- **Tech Stack Confirmation**: Finalized the decision to use Flask for the backend and Redis for ephemeral key-value storage (essential for the self-destruct feature).
- **Repository Setup**: Initialized `onetimeshare` git repository and defined the project structure.
- **Planning**: Outlined the high-level 30-day roadmap.

---

## 📅 Day 1: Skeleton & Prototype (Dec 25, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Flask Setup**: Create the basic Flask application factory structure (`app/__init__.py`, `run.py`).
- [x] **Docker Initialization**: specific `Dockerfile` for the Flask app and a `docker-compose.yml` that includes the Redis service.
- [x] **Basic Upload Route**: Implement a minimal `/upload` endpoint that can accept a file via POST request.
- [x] **Redis Connection**: Verify connection between Flask and the Redis container.
- [x] **Health Check**: Ensure the application runs locally via `docker-compose up`.

---

## 📅 Day 2: Core Logic (Dec 26, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Secure File Saving**: Files saved to disk with UUID-based filenames.
- [x] **Extension Validation**: Only allow pdf, txt, png, jpg, jpeg, gif, env.
- [x] **File Size Validation**: Max 20MB limit via MAX_FILE_SIZE config.
- [x] **Redis Metadata Storage**: Store filename, content_type, upload_time using hset().
- [x] **TTL Expiration**: Auto-delete after 5 hours via REDIS_TTL.
- [x] **API Endpoints**: `/upload` (POST), `/info/<token>` (GET), `/list-files` (GET).
- [x] **Configuration**: config.py with environment variable support.

### Lessons Learned
- `import module` ≠ `from module import Class`
- `os.makedirs()` is NOT optional before file writes
- `decode_responses=True` required for Redis string responses

---

## 📅 Day 3: Link Generation & Architecture (Dec 27, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Service Layer Pattern**: Created `services/redis_service.py` with RedisService class.
- [x] **LinkGenerator**: Created `utils/link_generator.py` for URL generation.
- [x] **File Validation Utility**: Created `utils/get_uuid.py` with custom exceptions.
- [x] **Routes Refactored**: Updated routes to use services instead of direct Redis calls.
- [x] **TTL Expiration**: Implemented via `expire()` with configurable timeout.
- [x] **All Endpoints Working**: `/upload`, `/info/<token>`, `/download/<token>`, `/list-files`.

### Lessons Learned
- Service Layer Pattern: Routes handle HTTP, services handle business logic
- Python ≠ Java: No `extends` — use composition
- `__init__` has TWO underscores on each side
- Import paths: `from app.utils.x` not `from utils.x`
- Custom exceptions make debugging easier

---

## 📅 Day 4: Frontend UI (Dec 28, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Design System**: "Industrial Urgency" theme (dark charcoal + Safety Orange).
- [x] **AI Mockups**: Generated 4 mockups after Figma attempt failed.
- [x] **Base Template**: `base.html` with JetBrains Mono, industrial navbar.
- [x] **Upload Page**: `index.html` with containment card, drag-drop, progress bar.
- [x] **Download Page**: `download.html` showing file metadata.
- [x] **CSS**: 540 lines implementing design system.
- [x] **JavaScript**: Drag-drop, file validation, fetch upload, copy-to-clipboard.
- [x] **Route Updated**: `/download/<token>` now renders template with metadata.

### Lessons Learned
- `{% include %}` ≠ `{% extends %}` (Jinja templating)
- Event propagation: label inside div = double triggers
- AI is leverage, not replacement
- Frontend is a skill, not "easy mode"

---

## 📅 Day 5: Download/View Endpoint (Dec 29, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Download Route**: Created `/d/<token>` with `send_from_directory()`.
- [x] **Info Page Route**: Created `/download/<token>` to render dl.html.
- [x] **Security**: Path traversal protection via send_from_directory.
- [x] **Frontend**: Download button in dl.html + download.js handler.
- [x] **Original Filename**: Uses `download_name` parameter.
- [x] **Full Flow**: Upload → Link → Info Page → Download working.

### Lessons Learned
- **Restart Flask** after code changes!
- Two-route pattern: info page + file serve
- Save Redis results: `metadata = redis_service.get(...)` before using

---

## 📅 Day 6: Self-Destruct Mechanism (Dec 30, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Atomic Deletion**: Redis WATCH/MULTI/EXEC for race-safe deletion.
- [x] **File Deletion**: Remove file from disk after successful download.
- [x] **Orphan Cleanup**: Bidirectional sync (files ↔ metadata).
- [x] **Startup Cleanup**: Automatic cleanup on app restart.
- [x] **Custom 404**: Error page for expired/deleted files.
- [x] **Download Route Updated**: `/d/<token>` now deletes after serving.

### Critical Bug Fixed
```diff
- directory=Config.UPLOAD_FOLDER
+ directory_path = current_app.config['UPLOAD_FOLDER']
```
Found through testing — files were not deleting because of wrong config reference!

### Lessons Learned
- `Config.UPLOAD_FOLDER` ≠ `current_app.config['UPLOAD_FOLDER']`
- `pipeline.unwatch()` required after WATCH if no transaction
- Test like a user, not a developer
- 29 mistakes made, 29 fixed — iteration works

---

## 📅 Week 1: Foundation (Remaining Days)
**Focus**: Recap & Refactor

- **Day 7 (Dec 31): Recap & Refactor**
  - Code review of the week's work.
  - Manual testing of Upload → Link → Download → Delete flow.
  - Write `v0.1` documentation.

---

## 📅 Day 7: Code Review & Testing (Dec 31, 2025)
**Status**: ✅ Completed

### Tasks
- [x] **Code Review**: Reviewed Week 1 code quality and organization.
- [x] **Manual Testing**: Full upload → download → delete flow verification.
- [x] **Documentation**: Created Week 1 summary and v0.1 notes.
- [x] **Refactoring**: Cleaned up code structure and comments.

### Lessons Learned
- Weekly reviews prevent technical debt accumulation
- Manual testing catches issues automated tests miss
- Good documentation is an investment, not overhead

---

## 📅 Day 8: Atomic Operations & Concurrency (Jan 1, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Optimistic Locking**: Implemented Redis WATCH/MULTI/EXEC pattern.
- [x] **Race Condition Prevention**: Atomic download prevents double-access.
- [x] **Transaction Safety**: Pipeline-based operations for consistency.
- [x] **Testing**: Concurrent download simulation scripts.

### Lessons Learned
- Redis transactions prevent race conditions
- WATCH/MULTI/EXEC creates atomic blocks
- Optimistic locking > pessimistic locking for this use case
- Test concurrency explicitly, don't assume safety

---

## 📅 Day 9: Password Protection (Upload Phase) (Jan 2, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Bcrypt Integration**: Installed and configured password hashing.
- [x] **PasswordUtils Class**: Created hash_password() and check_hash().
- [x] **Redis Schema Update**: Added password_hash and is_protected fields.
- [x] **Upload Route**: Capture and hash passwords on upload.
- [x] **Frontend UI**: Password checkbox, input, visibility toggle.
- [x] **Type Fixes**: Converted bool → string for Redis compatibility.
- [x] **Docker Healthcheck**: Fixed service dependency race.

### Critical Bugs Fixed
1. Hardcoded variables instead of using calculated values
2. Redis type error (bool → "True"/"False")
3. Missing @staticmethod decorators
4. Docker race condition (healthcheck added)

### Lessons Learned
- Redis only accepts: bytes, str, int, float (NOT bool or None!)
- Variables must be USED, not just calculated
- Docker healthchecks prevent race conditions
- Test the complete loop, not just one half

---

## 📅 Day 10: Password Verification Logic (Jan 3, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Download Route Refactor**: Fixed premature deletion bug.
- [x] **Three-Route Architecture**: `/d/<token>`, `/download/<token>`, `/verify/<token>`.
- [x] **Password Verification**: Implemented bcrypt check on download.
- [x] **Retry Limit System**: Max 5 attempts with Redis persistence.
- [x] **Helper Function**: Created serve_and_delete() for reusability.
- [x] **Templates**: password.html, max_retries.html, invalid_password.html.
- [x] **Redis Fix**: Fixed WRONGTYPE error in cleanup function.

### 26 Bugs Fixed Across 6 Passes
- **Pass 1 (8 bugs)**: Premature deletion, GET/POST confusion, wrong function signatures
- **Pass 2 (5 bugs)**: Variable name errors, undefined response, incomplete logic
- **Pass 3 (4 bugs)**: Syntax errors, missing imports, missing returns
- **Pass 4 (7 bugs)**: HTTP statelessness issue (local variable won't persist!)
- **Pass 5 (1 bug)**: Forgot attempt_to_unlock in store_file_metadata()
- **Pass 6 (1 bug)**: Not checking Redis key type before hgetall()

### Critical Insight
**HTTP is stateless!** Local variables reset on every request. Use Redis for cross-request persistence.

```python
# ❌ WRONG - cnt resets every request
cnt = 0
cnt += 1

# ✅ CORRECT - persists in Redis
attempts = int(metadata.get('attempt_to_unlock', 0))
attempts += 1
metadata['attempt_to_unlock'] = str(attempts)
redis_service.store_file_metadata(token, metadata)
```

### Lessons Learned
1. **HTTP is stateless** - Use Redis, not local variables
2. **Test early** - Would have caught bugs sooner
3. **Fix bugs before features** - Don't build on broken code
4. **Redis stores strings** - Always convert types
5. **Function signatures matter** - Update all call sites
6. **Check key types** - Not all Redis keys are hashes

### Current Security Status
✅ **Production-Ready Password Protection:**
- Upload with bcrypt hashing (Day 9)
- Download with password verification (Day 10)
- Retry limit enforcement (5 attempts max)
- Atomic file deletion
- Proper error handling

---

## 📅 Day 11: Analytics & Frontend Polish (Jan 4, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Redis Counters**: Implemented 8 analytics counters (uploads, downloads, deletions).
- [x] **Stats Dashboard**: Created `/stats` endpoint with real-time metrics.
- [x] **Stats JSON API**: Created `/stats-json` for AJAX refresh.
- [x] **Protected Badge**: Shows "🔒 PASSWORD PROTECTED" on success page.
- [x] **Copy Button**: Added clipboard copy with visual feedback toast.
- [x] **Error Page**: Created `error.html` template for service errors.
- [x] **Counter Reset**: Reset analytics on container startup (RDB persistence fix).
- [x] **Navbar Update**: Added STATS link to navigation.

### 5 Passes to Completion
- **Pass 1 (C+)**: 11 bugs - counter names mismatched, strings vs ints, module-level code
- **Pass 2 (B)**: 5 bugs - downloads/deletions not tracked, wrong key names
- **Pass 3 (A+)**: Fixed get_counter() return type, added all tracking
- **Pass 4 (A+)**: AI-generated frontend (stats dashboard, protected badge, copy toast)
- **Pass 5**: Fixed Redis persistence bug (counters reset on startup)

### Critical Bugs Fixed
1. Counter names must match EXACTLY (`uploads` ≠ `upload`)
2. Redis returns strings, not integers - always decode
3. Module-level code runs on every reload
4. RDB persistence preserves counters across restarts - reset needed

### Lessons Learned
1. **Counter consistency**: Set and get must use identical keys
2. **Redis types**: Always cast to int when retrieving counters
3. **Ephemeral data**: Reset counters on startup to avoid stale data
4. **AI leverage**: Frontend generated in 8 minutes vs 2 hours backend debugging

---

## 📅 Week 2: Core Features (Jan 1 - Jan 7)
**Focus**: One-time View Enforcement & Password Protection

- **Day 8 (Jan 1)**: ✅ Atomic operations (completed)
- **Day 9 (Jan 2)**: ✅ Password protection upload (completed)
- **Day 10 (Jan 3)**: ✅ Password verification logic (completed)
- **Day 11 (Jan 4)**: ✅ Analytics & frontend polish (completed)
- **Day 12 (Jan 5)**: Edge case handling (Redis failure, missing files).
- **Day 13 (Jan 6)**: UI optimization & refactoring.
- **Day 14 (Jan 7)**: Week 2 Testing & Bug Fixes.

---

## 📅 Week 3: Security & Polish (Jan 8 - Jan 14)
**Focus**: Encryption & Rate Limiting

- **Day 15 (Jan 8)**: Research and select File Encryption method (likely symmetrical encryption like Fernet/AES).
- **Day 16 (Jan 9)**: Implement Encryption-at-rest (encrypt file before saving to disk).
- **Day 17 (Jan 10)**: Implement Decryption-on-fly (decrypt stream when user downloads).
- **Day 18 (Jan 11)**: Add Flask-Limiter to prevent abuse (Rate limiting on upload/download endpoints).
- **Day 19 (Jan 12)**: UI Polish (Animations, Copy-to-clipboard buttons, better mobile responsiveness).
- **Day 20 (Jan 13)**: Security Audit (Dependency vulnerability scan, ensuring no secrets in code).
- **Day 21 (Jan 14)**: Week 3 Wrap-up & Performance testing.

---

## 📅 Week 4: Launch & Documentation (Jan 15 - Jan 24)
**Focus**: Production Ready & CI/CD

- **Day 22 (Jan 15)**: Docker Production Optimization (Gunicorn vs Dev Server).
- **Day 23 (Jan 16)**: Set up GitHub Actions for automated testing (Pytest).
- **Day 24 (Jan 17)**: Write comprehensive Unit Tests for core logic.
- **Day 25 (Jan 18)**: Deployment Config (Nginx reverse proxy setup).
- **Day 26 (Jan 19)**: Deployment Dry-Run (Test on a VPS or cloud provider).
- **Day 27 (Jan 20)**: Finalize `README.md` and documentation API.
- **Day 28 (Jan 21)**: Post-Launch Polish (Feedback widgets, analytics if privacy-compliant).
- **Day 29 (Jan 22)**: Prepare Launch content (Screenshots, Demo Video).
- **Day 30 (Jan 24)**: **PUBLIC LAUNCH** - Release v1.0.0.

---

## 📝 Daily Adaptation Template

Copy this into your daily log to track progress and blockers.

```markdown
### Evening Review Questions (Answer daily):
- **What surprised me today?** (Technical or feedback)
  - 
- **What's blocking progress?**
  - 
- **What feedback should I act on immediately?**
  - 
- **What can I simplify tomorrow?**
  - 
- **What should I learn tonight to unblock tomorrow?**
  - 

### Morning Planning Questions:
- **Based on yesterday, what needs to change today?**
  - 
- **What's the most valuable single thing I can complete?**
  - 
- **Who can help me with today's challenges?**
  - 
- **What's the simplest implementation that works?**
  - 
- **How can I share today's progress compellingly?**
  - 
```