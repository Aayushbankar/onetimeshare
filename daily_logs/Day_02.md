# 📅 Day 2: Core Logic
**Date**: December 26, 2025
**Focus**: Secure File Saving, Unique IDs, Redis Metadata Structure

---

## 🎯 Daily Goals
By the end of today, you should have:
1.  **Secure File Saving**: Files uploaded via the `/upload` endpoint are saved to disk with unique identifiers.
2.  **Unique ID Generation**: A robust system for creating unpredictable, unique file IDs.
3.  **Redis Metadata**: A clear data structure stored in Redis containing file metadata.
4.  **File Retrieval Proof**: Ability to retrieve file info from Redis using the unique ID.

---

## 📋 Task List

### 1. File Upload & Saving
- [x] Create a dedicated `uploads/` directory for storing files.
- [x] Update `/upload` endpoint to actually save the file to disk.
- [x] Generate a unique ID (UUID) for each uploaded file.
- [x] Rename/save files using the unique ID (not the original filename for security).

### 2. Redis Metadata Structure
- [x] Define the metadata schema for Redis (filename, content_type, upload_time).
- [x] Store metadata in Redis using the unique ID as the key.
- [x] Set up `/info/<token>` route to verify metadata storage and retrieval.
- [x] **BONUS**: Added `/list-files` route to list all stored files.
- [x] **BONUS**: Added TTL (5-hour expiration) via `Config.REDIS_TTL`.

### 3. File Validation
- [x] Add extension validation using `ALLOWED_EXTENSIONS`.
- [x] Implement file size limit via `MAX_FILE_SIZE` (20MB).
- [x] Return appropriate JSON error messages for invalid uploads.

### 4. Configuration
- [x] Create `config.py` with environment variable support.
- [x] Load configuration via `app.config.from_object()`.
- [x] Ensure the upload folder is created if it doesn't exist (`os.makedirs`).
- [x] Added `MAX_FILE_SIZE` and `REDIS_TTL` config values.

---

## 🧠 Learning Objectives (Documented)

### **1. File Handling in Flask**
*   **Concept**: Flask uses `request.files` to access uploaded files via `FileStorage` objects.
*   **Key Takeaway**: The file stream can only be read once! Use `file.seek(0)` to reset.

### **2. UUID Generation**
*   **Concept**: `uuid.uuid4()` generates 122 bits of randomness.
*   **Why**: Makes file links practically impossible to guess — critical for security.
*   **Implementation Status**: ✅ Successfully implemented!

### **3. Configuration Management**
*   **Concept**: Centralize settings in a Config class with environment variable fallbacks.
*   **Pattern Used**: `os.environ.get('KEY', 'default')`
*   **Lesson Learned**: Access via `current_app.config` for consistency.

### **4. Path Security**
*   **Concept**: Never trust `file.filename` directly — it's user input!
*   **Solution**: Use UUID-based filenames, preserving only the extension.

---

## 🔴 Mistakes Made Today

### **Mistake #1: Syntax Error in Config**
*   **Issue**: Trailing period in `config.py`: `{'pdf', 'txt', ...}.`
*   **Root Cause**: Typo during editing.
*   **Solution**: Remove the period.
*   **Prevention**: Run `python -c "import config"` to syntax check.

### **Mistake #2: Variable Shadowing (Import Confusion)**
*   **Issue**: In `utils.py` — `import config` then later `config = Config()`
*   **Root Cause**: Confusion between module name and class name.
*   **Solution**: Use `from config import Config` and different variable names.
*   **Lesson**: Module import (`import x`) vs Class import (`from x import Y`).

### **Mistake #3: Incomplete Function**
*   **Issue**: `utils.py` function does nothing — no return, dead code.
*   **Root Cause**: Started coding without a clear plan.
*   **Solution**: Write pseudocode first, then implement.

### **Mistake #4: Inconsistent Config Access**
*   **Issue**: Mixing `Config.UPLOAD_FOLDER` (class attribute) and `current_app.config` patterns.
*   **Root Cause**: Not choosing one architectural pattern.
*   **Solution**: Stick with `current_app.config['KEY']` — Flask's standard.

### **Mistake #5: Missing Validation**
*   **Issue**: `ALLOWED_EXTENSIONS` defined but never checked!
*   **Root Cause**: Forgot to use the configuration.
*   **Solution**: Add `allowed_file()` helper function and call it before saving.

### **Mistake #6: No Redis Metadata Storage**
*   **Issue**: File saves to disk but metadata not stored in Redis.
*   **Root Cause**: Task incomplete — focused on file saving first.
*   **Solution**: Add `redis_client.hset()` call after `file.save()`.

### **Mistake #7: Inconsistent Error Responses**
*   **Issue**: Success returns JSON, error returns plain string with no status code.
*   **Root Cause**: Quick coding without thinking about API consistency.
*   **Solution**: Always return `jsonify({})` with explicit status codes.

---

## 📝 Documentation Requirements
*For your daily public post / log:*

1.  **Snippet**: UUID-based File Saving
    ```python
    token = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1].lower()
    stored_filename = f"{token}{ext}"
    file.save(os.path.join(Config.UPLOAD_FOLDER, stored_filename))
    ```

2.  **Output**: Successful Upload Response
    ```json
    {
        "status": "success",
        "filename": "550e8400-e29b-41d4-a716-446655440000.pdf",
        "content_type": "application/pdf"
    }
    ```

3.  **Insight**: 
    > "Integration is harder than understanding. I understood each piece — FileStorage, UUIDs, Redis hashes, Config patterns — but putting them together revealed gaps. Module imports vs class imports tripped me up. The key lesson: be consistent in your patterns and plan before you code."

4.  **Command**: Test upload with curl:
    `curl -X POST -F "file=@test.pdf" http://localhost:5000/upload`

---

## 📊 Day 2 Progress Report

| Task                   | Status     | Notes                       |
| ---------------------- | ---------- | --------------------------- |
| File saves to disk     | ✅ Done     | UUID filenames working      |
| Redis metadata storage | ❌ Not done | Next priority               |
| Extension validation   | ❌ Not done | Config ready, logic missing |
| Configuration system   | ✅ Done     | Minor syntax error to fix   |
| Error handling         | ⚠️ Partial  | Needs consistency           |

**Overall Progress**: ~58% of Day 2 goals achieved.

---

## 🎯 Tomorrow's Continuation
1. Fix the syntax error in `config.py`.
2. Add Redis metadata storage to `/upload`.
3. Implement extension validation.
4. Add `/info/<token>` route to verify metadata.
