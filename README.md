# 🚀 One-Time Secure File/Text Sharing App
> **30-Day Build Challenge**

![Status](https://img.shields.io/badge/Status-Live-success?style=flat-square)
![CI](https://github.com/Aayushbankar/onetimeshare/actions/workflows/ci.yml/badge.svg)
![Language](https://img.shields.io/badge/Language-Python-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Deployment](https://img.shields.io/badge/Deployment-Render-purple?style=flat-square)

> **🔴 LIVE DEMO**: [https://onetimeshare.onrender.com](https://onetimeshare.onrender.com)

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

## 🚀 Quick Start (Docker - Recommended)

The fastest way to run OneTimeShare is using Docker. This is the **recommended approach** for most users.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Aayushbankar/onetimeshare.git
cd onetimeshare
```

### Step 2: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your credentials
# REQUIRED: Set a secure SECRET_KEY and ADMIN_PASSWORD
nano .env  # or use your preferred editor
```

**Important Configuration:**
| Variable         | Required | Description                                     |
| ---------------- | -------- | ----------------------------------------------- |
| `SECRET_KEY`     | ✅ Yes    | Flask session secret (use a long random string) |
| `ADMIN_PASSWORD` | ✅ Yes    | Password for admin panel access                 |
| `ADMIN_USERNAME` | No       | Admin username (default: `admin`)               |
| `JWT_SECRET_KEY` | No       | JWT token secret for API auth                   |

### Step 3: Launch with Docker Compose
```bash
# Start all services (Flask app + Redis)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### Step 4: Access the Application
- 🌐 **Web App**: http://localhost:5000
- 🔐 **Admin Panel**: http://localhost:5000/auth/login
- 📊 **Stats Dashboard**: http://localhost:5000/stats

### Stop & Cleanup
```bash
# Stop services
docker-compose down

# Stop and remove all data (uploads + Redis)
docker-compose down -v
```

---

## 🛠️ Manual Installation (Development)

For local development without Docker:

### Prerequisites
- Python 3.10+
- Redis server running locally

### Setup
```bash
# Clone the repository
git clone https://github.com/Aayushbankar/onetimeshare.git
cd onetimeshare

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start Redis (in another terminal)
redis-server

# Run the application
python run.py
```

---

## 📖 Usage Guide

### Uploading a File
1. Navigate to http://localhost:5000
2. Drag & drop a file or click to select
3. (Optional) Set a password for additional security
4. Click **Upload**
5. Copy the generated unique link

### Downloading a File
1. Open the unique link
2. If password-protected, enter the password
3. Click **Download** — the file is permanently deleted after this!

### Admin Dashboard
1. Go to http://localhost:5000/auth/login
2. Login with your `ADMIN_USERNAME` and `ADMIN_PASSWORD`
3. View stats, manage files, and monitor system health

### API Endpoints
| Endpoint        | Method | Description                         |
| --------------- | ------ | ----------------------------------- |
| `/upload`       | POST   | Upload a file (multipart/form-data) |
| `/info/<token>` | GET    | Get file metadata                   |
| `/d/<token>`    | GET    | Download file (triggers deletion)   |
| `/stats-json`   | GET    | System statistics (JSON)            |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report Bugs**: Open an issue with steps to reproduce
- 💡 **Suggest Features**: Share ideas via GitHub Issues
- 📝 **Improve Docs**: Fix typos, clarify instructions
- 🔧 **Submit Code**: Fork, code, and open a Pull Request

### Development Workflow
```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/onetimeshare.git
cd onetimeshare

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and test
docker-compose up -d
# ... test your changes ...

# 5. Commit with a descriptive message
git add .
git commit -m "feat: add your feature description"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Open a Pull Request on GitHub
```

### Code Guidelines
- Follow existing code style and patterns
- Add comments for complex logic
- Update documentation if adding new features
- Test your changes before submitting

### Commit Message Format
```
type: brief description

Types: feat, fix, docs, style, refactor, test, chore
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

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
- **Day 12 (Jan 5)**: ✅ Edge case handling (completed)
- **Day 13 (Jan 6)**: ✅ Admin authentication (completed)
- **Day 14 (Jan 7)**: ✅ Week 2 Testing & Bug Fixes (completed)

---

## 📅 Day 12: Edge Case Handling & Security (Jan 5, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Redis Error Handler**: `@handle_redis_error` decorator with comprehensive error catching.
- [x] **Custom Error Pages**: Created 503.html, 500.html for graceful failures.
- [x] **Security Audit**: Removed unsafe `/admin` and `/test-redis` routes.
- [x] **Frontend Error Handling**: JS redirects to error pages.
- [x] **Config Fix**: Synchronized MAX_CONTENT_LENGTH to 20MB.

### Lessons Learned
- `@wraps(f)` is required for Flask decorators
- Configuration should be Single Source of Truth
- Test like a user, not a developer

---

## 📅 Day 13: Admin Authentication (Jan 6, 2026)
**Status**: ✅ Completed

### The Pivot
Started with SQLAlchemy database approach, then realized config-based auth is simpler for single-admin apps.

### Key Features Built
- **Config-Based Auth**: Admin credentials in `.env` file
- **Flask-Login**: Browser session management
- **JWT Support**: API token authentication
- **@admin_required Decorator**: Protects admin routes
- **Auto-Logout Security**: Session expires when leaving admin routes
- **Admin Dashboard**: Stats, file list, navigation
- **Zero-Knowledge Privacy**: Admins see tokens, not filenames

### Files Created
```
NEW:
├── app/auth/
│   ├── __init__.py
│   ├── routes.py        # Login, logout, dashboard
│   ├── decorators.py    # @admin_required
│   └── admin_user.py    # Simple user class
├── app/templates/admin/
│   ├── login.html
│   ├── dashboard.html
│   └── list_files.html
└── .env.example

MODIFIED:
├── config.py            # ADMIN_USERNAME, ADMIN_PASSWORD
├── app/__init__.py      # Flask-Login, auto-logout
├── app/routes.py        # @admin_required on routes
├── docker-compose.yml   # Env vars, volumes, retry
└── requirements.txt     # flask-login, flask-jwt-extended
```

### Time Analysis
- **Total**: 4h 20min (11:30-12:20 + 13:30-17:00)
- **6 Passes**: C → B+ → A → B → A → A
- **Key Insight**: 2h "wasted" on SQLAlchemy, but valuable learning

### Lessons Learned
- Ask "What's the simplest solution?" before choosing technology
- Circular imports happen — keep shared code in separate modules
- Docker services may start before network DNS is ready — add retry logic

---

## 📅 Day 14: Week 2 Testing & Security Fixes (Jan 7, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Integration Testing**: All 9 critical flows tested (upload, download, password, retry, admin).
- [x] **Critical Bug #1**: Fixed retry counter bypass (URL revisit allowed re-entering password).
- [x] **Critical Bug #2**: Fixed DoS vulnerability (reverted file deletion on max retries → implemented locking).
- [x] **Medium Bug**: Fixed Redis DNS startup race condition.
- [x] **Documentation**: Created pass analysis diagrams and mistake logs.

### Key Security Fix
**Before**: Users could delete ANY file by exhausting retries (DoS vulnerability).
**After**: Files are LOCKED on max retries, not deleted. Entry point blocks access.

### Lessons Learned
- Availability = Security (CIA Triad) — deleting to "secure" violates availability
- Think like an attacker: "Can I grief the user by spamming this?"
- Locking > Deleting for abuse prevention

---

## 📅 Week 3: Security & Polish (Jan 8 - Jan 14)
**Focus**: Encryption & Rate Limiting

---

## 📅 Day 15: File Encryption Research (Jan 8, 2026)
**Status**: ✅ Completed

### Research Completed
- Studied production patterns: Signal, Bitwarden, Microsoft 365
- Compared algorithms: AES-256-GCM vs ChaCha20-Poly1305
- Evaluated KDFs: Argon2id vs PBKDF2 vs bcrypt
- Analyzed Python libraries: Fernet vs hazmat primitives
- Designed streaming encryption for large files

### Architecture Decisions

| Component        | Choice            | Rationale                                 |
| ---------------- | ----------------- | ----------------------------------------- |
| **Algorithm**    | ChaCha20-Poly1305 | Constant-time, no AES-NI needed           |
| **KDF**          | Argon2id          | Memory-hard, GPU-resistant                |
| **Key Approach** | Hybrid            | Optional password (zero-knowledge if set) |
| **Chunking**     | 64KB              | Memory-efficient streaming                |

### Real Incidents Studied
- Nonce reuse (184 HTTPS servers vulnerable)
- Heartbleed (OpenSSL buffer over-read)
- Uber GitHub leak (hardcoded credentials)
- Capital One breach (encryption without proper IAM)

### Lessons Learned
- Encryption is easy; key management is where apps die
- One bug = total failure in crypto
- Zero-knowledge shifts responsibility to users
- Chunking essential for memory efficiency at scale

---

## 📅 Day 16: File Encryption Implementation (Jan 9, 2026)
**Status**: ✅ Completed

### Feature Built
End-to-end file encryption using ChaCha20-Poly1305:
- **Upload**: Files encrypted before saving to disk
- **Download**: Streaming decryption on-the-fly
- **Password Mode**: Argon2id key derivation (zero-knowledge)
- **Server Mode**: Random 256-bit key stored in Redis

### Architecture Decisions
- **Algorithm**: ChaCha20-Poly1305 (faster/safer than AES-GCM on software)
- **Key Derivation**: Argon2id (memory-hard password hashing)
- **Chunking**: 64KB chunks for low-memory streaming

### Critical Lesson: Flask Streaming Pattern
```python
# ❌ WRONG - Response inside generator
def generate():
    yield chunk
    return Response(generate())  # Infinite recursion!

# ✅ CORRECT - Response outside generator
def generate():
    yield chunk
return Response(generate())  # Outside!
```

---

## 📅 Day 17: Rate Limiting & UI Polish (Jan 10, 2026)
**Status**: ✅ Completed

### Features Built
1.  **Rate Limiting Engine**:
    - Integrated `Flask-Limiter` with Redis backend
    - Limits: 5 uploads/hour, 60 downloads/minute
    - Custom `429.html` error page
2.  **Admin Analytics**:
    - Real-time "Limit Hits" counter in stats dashboard
3.  **UI Redesign (Pass 6)**:
    - Standardized ALL 9 error pages (404, 500, 403, 410, etc.)
    - Applied "Industrial Dark" theme (screws, containment cards)

### 6 Bugs Fixed
- **Critical**: Flask-Limiter 3.x breaking changes (storage_uri deprecation)
- **Critical**: Hardcoded Redis host in config
- **UX**: Inconsistent error page styling (Fixed by redesign)

### Lessons Learned
- **Breaking Changes Happen**: Libraries evolve (Flask-Limiter 3.0 changed init pattern)
- **Redis Keys**: Default limiter prefix is `LIMITS:LIMITER*`, not `LIMITER:*`
- **Visual Consistency**: Error pages are part of the product experience

---

## 📅 Day 18: UI Polish & Motion Design (Jan 11, 2026)
**Status**: ✅ Completed

### Features Built
- **Motion System**: CSS-only `slideUpFade` entrance animations.
- **Micro-interactions**: Tactile button feedback, instant copy verification.
- **Mobile Overhaul**: Stacked navbar, dynamic padding, responsive grids.
- **Page Redesigns**: Password & Max Retries pages fully themed.

### Metrics
- **Performance**: 96/100 Lighthouse
- **CSS Size**: +2KB
- **Mistakes**: 1 (Grepping for JS classes)

---

## 📅 Day 19: Security Audit (Jan 12, 2026)
**Status**: ✅ Completed

### Tasks
- [x] **Dependency Scan**: Patched 3 vulnerabilities (urllib3).
- [x] **Secret Scanning**: Rotated hardcoded secrets to `.env`.
- [x] **Network Hardening**: Closed exposed Redis port 6379.
- [x] **Config Security**: Enforced HTTPOnly cookies.

### Outcome
- **Grade**: A (System fully secured)
- **Findings**: 3 CVEs patched, keys rotated

---

## 📅 Day 20: Week 3 Wrap-up & Performance (Jan 13, 2026)
**Status**: ✅ Completed

### 🎯 Achievements
- **Platinum Certified Performance**: 218 RPS @ 421ms Latency (Pass 3)
- **Infrastructure**: Gunicorn Migration + Redis Rate Limiting
- **Report**: [Load Testing Certification](docs/Day_20_Load_Testing_Report.md)

---

---

## 📅 Day 21 (Jan 14): Makar Sankranti (Break Day) 🪁
**Status**: ⏸️ Resting
- **Activity**: Kites, Til-gul, and No Code.

---

## 📅 Week 4: Launch & Documentation (Jan 15 - Jan 24)
**Focus**: Production Ready & CI/CD

> **Note**: Gunicorn optimization (218 RPS) and Render deployment were completed in Day 20. Week 4 focuses on CI/CD, testing, and launch preparation.

---

## 📅 Day 22: CI/CD Setup + Stress Testing (Jan 15, 2026)
**Status**: ⚠️ Partially Complete

### 🎯 Completed: Comprehensive Stress Testing
9-pass stress test suite — **ALL GRADE A @ 0% ERROR RATE**

| Tier                  | Max Users | Peak RPS | P95 Latency | Grade |
| --------------------- | --------- | -------- | ----------- | ----- |
| **Tier 1** (Baseline) | 30        | 174.66   | 355ms       | A     |
| **Tier 2** (Peak)     | 100       | 116.44   | 1.3s        | A     |
| **Tier 3** (DDoS Sim) | 300       | 97.95    | 3.5s        | A     |

**Performance Ceiling**: 300 concurrent users @ ~100 RPS (hardware-bound)

### ❌ Deferred: CI/CD
Carried to Day 23 due to time constraints.

---

## 📅 Day 23: CI/CD Pipeline Setup (Jan 16, 2026)
**Status**: ✅ Completed

### 🎯 Features Built
1. **GitHub Actions Workflow**: `.github/workflows/ci.yml`
   - Python 3.12 setup with pip caching
   - Redis service container for tests
   - Triggers on push/PR to main/develop
2. **Test Verification**: 21/21 tests passing
3. **CI Badge**: Added to README header

### Key Configuration
```yaml
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

### Metrics
- **Tests**: 21 passing, 0 failures
- **Workflow**: 48 lines of YAML
- **Time**: ~30 minutes implementation

---

---

## 📅 Day 24: Integration & E2E Testing (Jan 17, 2026)
**Status**: ✅ Completed

### 🎯 Features Built
1. **End-to-End Testing**:
   - Implemented `pytest-playwright` suite.
   - Verified **Upload -> Download -> Expiry** lifecycle.
   - Fixed production Rate Limit conflicts during testing.
2. **Coverage Reporting**:
   - Added `pytest-cov` and API Integration tests (`tests/integration/`).
   - Achieved backend coverage metrics (verification pending full suite run).
3. **Documentation**:
   - Created beginner guides for Headless Browsers & Playwright.

### Metrics
- **E2E Tests**: 2 Suites (Upload, Download)
- **Integration**: 1 Suite (API Routes)
- **Mistakes**: 3 (Environment & Selectors)

---

### Week 4 Roadmap
- ✅ **Day 24 (Jan 17)**: Integration & E2E Tests — **Completed**.
- 🚧 **Day 25 (Jan 18)**: Security Hardening — cURL blocking, Defense-in-Depth Audit, Security Headers.
- **Day 26 (Jan 19)**: QC & Reporting — HTML Test Reports, Coverage Dashboards.
- **Day 27 (Jan 20)**: Documentation Finalization — API docs, changelog, diagrams.
- **Day 28 (Jan 21)**: Demo Video & Screenshots — Marketing assets.
- **Day 29 (Jan 22)**: Beta Testing & Feedback — Share with select users.
- **Day 30 (Jan 24)**: **🚀 PUBLIC LAUNCH** - Release v1.0.0.

---

