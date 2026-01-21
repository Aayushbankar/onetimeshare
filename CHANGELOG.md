# Changelog

All notable changes to OneTimeShare are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-01-24 (Upcoming)
### 🚀 Production Release
The culmination of the 30-Day Build Challenge.

---

## [0.9.1] - 2026-01-21
### Added
- **Resilience**: Graceful Degradation (App survives Redis failure)
- **Reporting**: `pytest-html` integration for visual test reports
- **Coverage**: `pytest-cov` integration for CI artifacts
- **Docs Refactor**: Standardized `docs/development/` structure
- **OSS Standards**: Created `CONTRIBUTING.md`

### Fixed
- Redis `ConnectionError` causing app crash (500)
- Flask-Limiter startup failure when Redis is down

---

## [0.9.0] - 2026-01-20
### Added
- **API Documentation** (`docs/API.md`)
- **Changelog** (`CHANGELOG.md`)
- Architecture diagrams

### Changed
- Day 26 skipped (health break)

---

## [0.8.0] - 2026-01-18
### Added
- **CLI Blocking**: Block `curl`/`wget` access to protected routes (HTTP 406)
- **Security Headers**: CSP, HSTS, X-Frame-Options middleware
- **Defense in Depth** architecture

### Fixed
- Integration test assertion mismatch (`test_cli_blocking.py`)
- Dockerfile port binding (dynamic `${PORT:-5000}`)

---

## [0.7.0] - 2026-01-17
### Added
- **End-to-End Testing**: Playwright test suite
- **Integration Tests**: API route coverage
- `pytest-playwright` and `pytest-cov` integration

---

## [0.6.0] - 2026-01-16
### Added
- **CI/CD Pipeline**: GitHub Actions workflow
- Redis service container for tests
- CI badge in README

---

## [0.5.0] - 2026-01-15
### Added
- **Stress Testing**: 9-pass load test suite
- Performance benchmarks (218 RPS @ 300 users)

---

## [0.4.0] - 2026-01-13
### Added
- **Gunicorn**: Production WSGI server
- **Load Testing**: Locust benchmark suite
- Performance optimization (4 workers, 2 threads)

---

## [0.3.5] - 2026-01-12
### Added
- **Security Audit**: Dependency scanning with `pip-audit`
- Secret rotation and `.env` hardening
- Network hardening (closed Redis port 6379)

---

## [0.3.4] - 2026-01-11
### Added
- **Motion Design**: CSS animations (`slideUpFade`)
- Mobile-responsive redesign
- Micro-interactions and visual polish

---

## [0.3.3] - 2026-01-10
### Added
- **Rate Limiting**: Flask-Limiter with Redis backend
- Custom `429.html` error page
- Rate limit analytics counter

### Changed
- Standardized all 9 error pages with industrial theme

---

## [0.3.2] - 2026-01-09
### Added
- **File Encryption**: ChaCha20-Poly1305 encryption at rest
- **Password Mode**: Argon2id key derivation (zero-knowledge)
- Streaming encryption for large files (64KB chunks)

---

## [0.3.1] - 2026-01-08
### Added
- Encryption research and architecture design
- Algorithm comparison (AES-GCM vs ChaCha20)
- Security incident case studies

---

## [0.3.0] - 2026-01-07
### Added
- **Admin Authentication**: Config-based admin login
- **Flask-Login**: Session management
- **Flask-JWT-Extended**: API token auth
- Admin dashboard and file list pages
- Auto-logout security

---

## [0.2.5] - 2026-01-06
### Fixed
- Retry counter bypass vulnerability
- DoS vulnerability (file locking vs deletion)
- Redis DNS startup race condition

---

## [0.2.4] - 2026-01-05
### Added
- **Error Handling**: `@handle_redis_error` decorator
- Custom error pages (503, 500)
- Redis connection retry logic

### Security
- Removed unsafe test routes

---

## [0.2.3] - 2026-01-04
### Added
- **Analytics Dashboard**: 8 Redis counters
- `/stats` and `/stats-json` endpoints
- Protected file badge on success page
- Copy-to-clipboard with toast notification

---

## [0.2.2] - 2026-01-03
### Added
- **Password Verification**: bcrypt check on download
- **Retry Limit**: Max 5 attempts with Redis persistence
- Three-route architecture (`/d/`, `/download/`, `/verify/`)
- Error templates (password, max_retries, invalid_password)

### Fixed
- 26 bugs across 6 debugging passes
- HTTP statelessness issue (local var vs Redis)

---

## [0.2.1] - 2026-01-02
### Added
- **Password Protection (Upload)**: bcrypt hashing
- Redis schema update (`password_hash`, `is_protected`)
- Password UI with visibility toggle

### Fixed
- Docker healthcheck race condition

---

## [0.2.0] - 2026-01-01
### Added
- **Atomic Operations**: Redis WATCH/MULTI/EXEC
- Race condition prevention for concurrent downloads
- Concurrent download test scripts

---

## [0.1.5] - 2025-12-31
### Changed
- Code review and refactoring
- Week 1 documentation

---

## [0.1.4] - 2025-12-30
### Added
- **Self-Destruct**: Atomic deletion after download
- **Orphan Cleanup**: Bidirectional file/metadata sync
- Startup cleanup on app restart
- Custom 404 page for expired files

### Fixed
- Config reference bug (`Config.` vs `current_app.config`)

---

## [0.1.3] - 2025-12-29
### Added
- **Download Endpoint**: `/d/<token>` with `send_from_directory()`
- Download info page (`/download/<token>`)
- Original filename preservation

---

## [0.1.2] - 2025-12-28
### Added
- **Frontend UI**: Industrial dark theme
- Upload page with drag-drop
- Download page with file metadata
- 540 lines of CSS

---

## [0.1.1] - 2025-12-27
### Added
- **Service Layer**: `RedisService` class
- **Link Generator**: UUID-based secure URLs
- File validation utilities
- TTL expiration (5 hours)

---

## [0.1.0] - 2025-12-26
### Added
- **Core Upload Logic**: UUID filenames, extension validation
- **Redis Integration**: Metadata storage with hset()
- File size limit (20MB)
- API endpoints: `/upload`, `/info/<token>`, `/list-files`

---

## [0.0.1] - 2025-12-25
### Added
- **Project Skeleton**: Flask app factory
- **Docker Setup**: Dockerfile + docker-compose.yml
- Redis service container
- Basic health check

---

## [0.0.0] - 2025-12-24
### Added
- **Project Inception**: #OneTimeShare30 challenge launched
- Repository initialization
- Tech stack decision (Flask + Redis)
- 30-day roadmap
