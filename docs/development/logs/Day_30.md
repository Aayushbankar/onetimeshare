# Day 30: The Launch

## 📝 Status: IN PROGRESS

**Focus:** Final Polish, CI/CD Fixes, and Launch.

## 🚧 Progress Log

### 10:00 AM - CI/CD Forensics
- **Blocker:** CI pipeline failed with `FileNotFoundError` in `RedisService`.
- **Diagnosis:** The `cleanup_orphan_files` method was trying to scan the `uploads` folder before it existed. This happens because CI runners start clean.
- **Action:** 
    - Patched `app/services/redis_service.py` to be defensive (check if dir exists).
    - Updated `app/__init__.py` to auto-create the directory on startup.
    - **Status:** **FIXED**. verified with `pytest` run.

### 11:30 AM - CSRF & Session Hell (The "Prod is F*cked" Incident)
- **Blocker:** All uploads failing locally with `400 Bad Request`.
- **Diagnosis:** Triple failure chain:
    1.  `config.py` forced Secure Cookies (HTTPS only) on Localhost (HTTP) -> Cookies dropped.
    2.  `app.js` wasn't sending `X-CSRFToken` header.
    3.  `base.html` was missing the CSRF meta tag.
- **Action:**
    - Relaxed `SESSION_COOKIE_SECURE` for dev environments.
    - Injected CSRF token into base template.
    - Updated frontend JS to send the token.
    - **Status:** **FIXED**.
    - **Documentation:** Created [02_CSRF_Deep_Dive.md](../notes/Day_30/02_CSRF_Deep_Dive.md).

### Next Steps
- Generate final assets (Demo GIF, Screenshots).
- Tag v1.0.0.
