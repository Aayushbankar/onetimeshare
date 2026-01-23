# Day 30 Mistakes Log

## 1. Redis Orphan Cleanup Crash (CI/CD Failure)
**Issue:**  
The CI pipeline failed with `FileNotFoundError: [Errno 2] No such file or directory: '.../uploads'` during the application startup.

**Context:**  
The `RedisService` initializes and immediately runs `cleanup_orphan_files()` to ensure disk consistency. This method iterates over `os.scandir(current_app.config['UPLOAD_FOLDER'])`.

**Root Cause:**  
In the CI environment (and fresh local installs), the `uploads` directory is not guaranteed to exist before the app starts. The application factory was attempting to use this directory via `RedisService` before creating it.

**Fix:**  
1.  **Defensive Coding in Service:** Modified `RedisService.cleanup_orphan_files` to explicitly check `if not os.path.exists(...)` and return early with success (0 deletions) if the folder is missing.
2.  **App Factory Update:** Added `os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)` in `app/__init__.py` *before* the service initialization to ensure the directory is created on startup.

**Lesson:**  
Never assume external resources (directories, databases, files) exist during startup. Always implement existence checks or idempotent creation logic, especially for file-system dependent features.

---
