# 👓 Pull Request Review: OneTimeShare v1.0

**Reviewer**: Antigravity (Principal Engineer)
**PR Status**: ⚠️ **Changes Requested**
**Scope**: Dependencies, Infrastructure, Logic, Concurrency.

---

## 📦 Dependencies & Infrastructure

### 1. `requirements.txt`: Gunicorn Version Weirdness
```text
gunicorn==23.0.0
```
*   **Observation**: As of 2025, the latest stable Gunicorn is typically 22.x or 23.x. Ensure this isn't a typo or an unstable nightly build. If `23.0.0` is valid in 2026, ignore.
*   **Risk**: Low.

### 2. `docker-compose.yml`: Production Volume Mounts
```yaml
volumes:
  - ./config.py:/app/config.py
```
*   **Observation**: You are mounting a local file into the container at runtime.
*   **Risk**: **High (Mutation)**. If the container is compromised, an attacker could potentially overwrite `config.py` on the *host machine* if permissions allow.
*   **Fix**: For production, `COPY` the config in the Dockerfile. Do not mount it. Use environment variables for secrets (which you are doing, good).

### 3. Redis Isolation
```python
# redis_service.py
self.redis_client.flushdb()
```
*   **Risk**: `flushdb()` wipes the *entire* database index. If you ever share this Redis instance (e.g., specific DB index 0) with another service (like a Celery worker or another app), you will nuke their data too.
*   **Fix**: Use `SCAN` + `DELETE` on a specific key prefix (e.g., `ots:*`), or ensure strict DB index isolation in documentation.

---

## 🧠 Logic & Concurrency

### 4. The "Orphan Maker" Pattern (Delete Metadata First)
**File**: `app/services/redis_service.py`
```python
def delete_file_and_metadata(self, token):
    metadata = self.atomic_delete(token)  # <--- Point of No Return
    # ... logic ...
    if os.path.exists(file_path):
        os.remove(file_path)              # <--- What if this crashes?
```
*   **Scenario**:
    1.  App calls `atomic_delete(token)`. Redis key is GONE.
    2.  Server crashes (OOM, Power loss) *before* `os.remove`.
    3.  **Result**: File remains on disk forever. Since the Redis key is gone, your `cleanup_orphan_metadata` won't catch it. Your `cleanup_orphan_files` *will* catch it, but that runs periodically.
    *   **Improvement**: It's acceptable for now due to the cleanup job, but a more robust "Mark for Deletion" pattern (Set Redis TTL = 10s, then delete disk, then delete Redis) is preferred for high-reliability systems.

### 5. Memory Bomb in Cleanup
**File**: `app/services/redis_service.py`
```python
files_on_disk = os.listdir(current_app.config['UPLOAD_FOLDER'])
```
*   **Risk**: **OOM (Out of Memory)**. If you have 1,000,000 files in that directory, `os.listdir` creates a massive list of strings in RAM.
*   **Fix**: Use `os.scandir()` which returns an iterator/generator. It's faster and memory-efficient.

---

## 🛡️ Security

### 6. XSS Check (Passed ✅)
*   **Templates**: You are using `{{ variable }}` (auto-escaped).
*   **JS**: You are using `.textContent = ...` (safe) instead of `.innerHTML`.
*   **Verdict**: Good frontend hygiene.

### 7. TOCTOU in Deletion
**File**: `app/utils/serve_and_delete.py`
```python
if os.path.exists(file_path):  # Check
    os.remove(file_path)       # Act
```
*   **Risk**: Low in this layout, but theoretically another thread could delete it between the check and the act, raising `FileNotFoundError`.
*   **Fix**: Wrap `os.remove` in `try/except FileNotFoundError` and remove the `if exists` check. It's faster (Ask Forgiveness, Not Permission).

---

## 📝 Summary of Changes Requested

1.  **Refactor**: Change `os.listdir` to `os.scandir` in cleanup jobs.
2.  **Hardening**: Remove `config.py` bind mount in `docker-compose.yml`.
3.  **Safety**: Wrap `os.remove` in try/except instead of checking `os.path.exists`.

**Approval Status**: **Pending Fixes**
