# 🛡️ OneTimeShare Audit & "Mistakes Found" Log

**Date**: 2026-01-21
**Auditor**: Antigravity (Pentester & Defense-in-Depth Architect)
**Scope**: Full Codebase Audit (`app/`)

---

## 🚨 Critical Security Vulnerabilities (CVSS 9.0+)

### 1. "Homebrewed" Crypto: XOR Nonce Construction
- **Location**: `app/utils/encryption_utils.py:40`
- **Code**: `new_nonce_int = base_nonce ^ counter`
- **Vulnerability**: You are modifying the ChaCha20 nonce by XORing it with a counter. This is **non-standard** and potentially dangerous. If `base_nonce` is random, XORing it with small integers *might* be unique, but it violates the "standard increment" design of counter-mode nonces.
- **Why it matters**: In cryptography, "rolling your own" arithmetic usually leads to collisions. A nonce collision in ChaCha20 destroys key stream security, allowing an attacker to decrypt the data.
- **Fix**: Use standard arithmetic addition (big-endian), or use the `sequence_number` parameter provided by many crypto libraries if available, or simply `nonce = base_nonce + counter`.

### 2. Admin Auth Timing Attack
- **Location**: `config.py:43`
- **Code**: `username == cls.ADMIN_USERNAME and password == cls.ADMIN_PASSWORD`
- **Vulnerability**: Python's string comparison operator (`==`) returns as soon as a byte mismatch is found. An attacker can measure the time it takes for the request to return to guess the password one character at a time.
- **Fix**: Use `secrets.compare_digest(password, cls.ADMIN_PASSWORD)` for constant-time comparison.

### 3. Server-Side Encryption Masquerading as E2EE
- **Location**: `app/utils/encryption_utils.py:12`
- **Finding**: `generate_key()` runs on the server.
- **Impact**: You claim "Secure" sharing, but the server (and by extension, you) possess the keys to decrypt any file that isn't password-protected. If the server is compromised, all active files are compromised.
- **Fix**: Real End-to-End Encryption (E2EE) requires generating the key in the **Browser** (WebCrypto API), uploading *encrypted* blobs, and putting the key in the URL anchor (`#key`) which is never sent to the server.

---

## ⚠️ High Architectural Risks (CVSS 7.0-8.9)

### 4. The "Lying" Health Check
- **Location**: `app/routes.py:72`
- **Code**: `return "OK", 200`
- **Finding**: This endpoint returns 200 OK even if Redis is down, Disk is full, or the database is on fire.
- **Impact**: In a container orchestration environment (Kubernetes/Docker Swarm), the orchestrator will think the app is healthy and keep sending it traffic, which will result in 100% error rates for users.
- **Fix**: The health check MUST ping Redis and check write permissions. Fallback to 503 if dependencies are down.

### 5. JWT Session Invalidation on Restart
- **Location**: `config.py:34`
- **Code**: `os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))`
- **Finding**: If `JWT_SECRET_KEY` is not set in `.env`, a new random key is generated every time the server restarts.
- **Impact**: Every time you deploy or restart the container, **every logged-in admin is kicked out immediately**. This is terrible UX and makes "rolling updates" impossible.
- **Fix**: Enforce `JWT_SECRET_KEY` existence in `.env` or use a persistent filesystem fallback.

---

## 🐛 Code Quality & Logic "Mistakes"

### 6. Crash on Files Without Extensions
- **Location**: `app/utils/get_uuid.py:28`
- **Code**: `file.filename.rsplit('.', 1)[1]`
- **Bug**: If a user uploads a file named `README` (no extension), `rsplit` returns a list of length 1. Accessing index `[1]` throws `IndexError`.
- **Result**: 500 Internal Server Error for valid files without extensions.

### 7. Content-Length Spoofing
- **Location**: `app/utils/get_uuid.py:33`
- **Code**: `if file.content_length > Config.MAX_FILE_SIZE:`
- **Bug**: `file.content_length` relies on the `Content-Length` header sent by the client. An attacker can send a 10GB file but declare `Content-Length: 100`.
- **Fix**: You must count bytes as you read/save the stream (using `Werkzeug`'s `LimitedStream` or checking file size after save, though saving 10GB first is a DoS vector).

### 8. UX-Breaking Error Handling
- **Location**: `app/routes.py:34` (`@handle_redis_error`)
- **Bug**: The decorator catches errors and returns `jsonify({"error": ...})`.
- **Impact**: If Redis fails during a **User Download** (GET request from browser), the user sees a raw JSON string `{ "error": "Redis..." }` instead of a styled `503.html` page.
- **Fix**: Check `request.accept_mimetypes` or context to decide whether to return JSON or render a Template.

### 9. Encapsulation Violation
- **Location**: `app/utils/serve_and_delete.py`
- **Finding**: This "Utility" function is doing everything: decrypting, deriving keys, talking to Redis, incrementing counters, and deleting files.
- **Impact**: It makes unit testing impossible because you can't test "serving" without mocking the entire Redis universe.

### 10. Commented-Out Zombie Code
- **Location**: `app/utils/encryption_utils.py:50-60`
- **Finding**: Large blocks of commented-out logic committed to the main branch.
- **Impact**: Reduces readability and indicates a lack of code cleanup discipline.

---

## 📉 Operational Mistakes

### 11. Logging Hygiene
- **Finding**: While not found in the limited grep, the `get_uuid` logger uses `logging.basicConfig`. If not configured properly in production, this might log to `stderr` which gets captured by Docker/CloudWatch.
- **Risk**: Ensure no filenames or sensitive tokens are logged in INFO/DEBUG levels (Privacy leak).

---

## ✅ Recommended "Go Deeper" Fixes

1.  **Rewrite Crypto**: Switch to `NaCl` (PyNaCl) or usage of `cryptography`'s high-level recipes instead of manual distinct calls.
2.  **Strict Type Checking**: Add `mypy` to your CI pipeline. You have type confusion in Redis (strings vs ints).
3.  **Chaos Engineering**: Actually kill Redis while the app is running and verify the "Graceful Degradation" manually.
