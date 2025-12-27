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

## 📅 Week 1: Foundation (Remaining Days)
**Focus**: UI, Download & Self-Destruct

- **Day 4 (Dec 28): Basic UI**
  - Set up Bootstrap 5 templates.
  - Create the `index.html` (Upload Interface) with a progress bar or simple file input.

- **Day 5 (Dec 29): Download/View Endpoint**
  - Create the download route `/d/<token>`.
  - Implement logic to look up file metadata from Redis using the token.

- **Day 6 (Dec 30): Self-Destruct Mechanism**
  - Implement the "Delete after read" logic (delete file from disk and key from Redis after successful download).
  - Configure Redis TTL (Time To Live) as a fallback for files that are never downloaded (e.g., 24-hour expiry).

- **Day 7 (Dec 31): Recap & Refactor**
  - Code review of the week's work.
  - Manual testing of the full Upload -> Link -> Download -> Delete flow.
  - Write `v0.1` documentation.

---

## 📅 Week 2: Core Features (Jan 1 - Jan 7)
**Focus**: One-time View Enforcement & Password Protection

- **Day 8 (Jan 1)**: Refine "One-Time" logic to strictly enforce single use (atomic operations in Redis).
- **Day 9 (Jan 2)**: Add optional Password Protection field to the Upload UI.
- **Day 10 (Jan 3)**: Implement backend password hashing and verification for protected files.
- **Day 11 (Jan 4)**: Create the "Enter Password" intermediate page for protected links.
- **Day 12 (Jan 5)**: Data validation (file size limits, allowed extensions).
- **Day 13 (Jan 6)**: Improve Error Handling (404 pages for expired links, 500 pages).
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