# Backend Routes Documentation

**Last Updated**: January 10, 2026  
**File**: `app/routes.py`  
**Total Routes**: 12

---

## 🗺️ Route Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           🌐 PUBLIC ROUTES                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   /  ──────────▶  /upload  ──────────▶  returns token                      │
│   (home)          (POST file)           (/d/<token>)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           📥 DOWNLOAD FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   /d/<token>  ────▶  is_protected?                                          │
│                           │                                                 │
│                     ┌─────┴─────┐                                           │
│                     │           │                                           │
│                     ▼           ▼                                           │
│                   YES          NO                                           │
│                    │            │                                           │
│                    ▼            │                                           │
│   /download/<token>             │                                           │
│   (password.html)               │                                           │
│         │                       │                                           │
│         ▼                       │                                           │
│   /verify/<token>               │                                           │
│         │                       │                                           │
│    ┌────┴────┐                  │                                           │
│    │         │                  │                                           │
│  correct   wrong                │                                           │
│    │         │                  │                                           │
│    │    retry/lock              │                                           │
│    │                            │                                           │
│    └──────────┬─────────────────┘                                           │
│               ▼                                                             │
│        serve_and_delete()                                                   │
│        (stream + delete)                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🔐 ADMIN ROUTES                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│   /stats          →  Analytics dashboard                                    │
│   /stats-json     →  Analytics JSON                                         │
│   /list-files     →  File list (anonymized)                                 │
│   /info/<token>   →  File metadata JSON                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           ⚠️ ERROR HANDLERS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│   404, 500        →  Global error handlers                                  │
│   /error/<code>   →  Render error page for JS redirects                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Quick Reference

| Route               | Method   | Auth   | Purpose                            |
| ------------------- | -------- | ------ | ---------------------------------- |
| `/`                 | GET      | Public | Home page                          |
| `/upload`           | POST     | Public | Upload file, encrypt, return token |
| `/d/<token>`        | GET      | Public | Download entry point               |
| `/download/<token>` | GET      | Public | Render download page               |
| `/verify/<token>`   | GET/POST | Public | Password verification              |
| `/list-files`       | GET      | Admin  | List all files                     |
| `/info/<token>`     | GET      | Admin  | Get file metadata JSON             |
| `/stats`            | GET      | Admin  | Stats dashboard                    |
| `/stats-json`       | GET      | Public | Stats as JSON                      |
| `/error/<code>`     | GET      | Public | Error pages                        |

---

## 📂 Detailed Route Documentation

### Index

1. [/ (Home)](#-1--home)
2. [/upload](#-2-upload)
3. [/d/\<token\>](#-3-dtoken)
4. [/download/\<token\>](#-4-downloadtoken)
5. [/verify/\<token\>](#-5-verifytoken)
6. [/list-files](#-6-list-files)
7. [/info/\<token\>](#-7-infotoken)
8. [/stats](#-8-stats)
9. [/stats-json](#-9-stats-json)
10. [/error/\<code\>](#-10-errorcode)

---

## 📖 1. `/` (Home)

**Method**: GET  
**Auth**: None  
**Template**: `index.html`

### Function
```python
@bp.route('/')
def index():
    redis_service.increment_counter("index_visits", 1)
    return render_template('index.html')
```

### Purpose
- Renders the upload page UI
- Tracks page visits in Redis

### Connections
- User uploads file → goes to `/upload`

---

## 📖 2. `/upload`

**Method**: POST  
**Auth**: None  
**Decorator**: `@handle_redis_error`

### Request
```
POST /upload
Content-Type: multipart/form-data

file: <binary>
password: <optional string>
```

### Response
```json
{
  "status": "success",
  "metadata": {
    "filename": "uuid.ext",
    "token": "uuid",
    "is_protected": "True/False",
    ...
  }
}
```

### Flow
```
1. Receive file
2. Generate UUID filename
3. If password provided:
   - Hash password (bcrypt)
   - Generate salt
   - Derive encryption key (Argon2id)
4. If no password:
   - Generate random encryption key
5. Encrypt file (ChaCha20-Poly1305)
6. Store metadata in Redis
7. Return token
```

### Connections
- Called from: `index.html` (JavaScript fetch)
- Returns: Token for `/d/<token>`

---

## 📖 3. `/d/<token>`

**Method**: GET  
**Auth**: None  
**Decorator**: `@handle_redis_error`

### This is the MAIN DOWNLOAD ENTRY POINT

### Flow
```
1. Get metadata from Redis
2. If not found → 410 Gone
3. If locked (max retries) → 403 Forbidden
4. If protected:
   - Redirect to password page
5. If unprotected:
   - Call serve_and_delete() → download file
```

### Connections
- If protected → renders `password.html` via `/download/<token>`
- If unprotected → calls `serve_and_delete()`

---

## 📖 4. `/download/<token>`

**Method**: GET  
**Auth**: None  
**Decorator**: `@handle_redis_error`

### Purpose
Renders the appropriate download page based on protection status.

### Flow
```
1. Get metadata
2. If not found → 404
3. If protected → render password.html
4. If unprotected → render dl.html
```

### Templates
- `password.html` — Password entry form
- `dl.html` — Direct download button

### Connections
- Called from: `/d/<token>` for protected files
- Password form submits to: `/verify/<token>`

---

## 📖 5. `/verify/<token>`

**Method**: GET, POST  
**Auth**: None  
**Decorator**: `@handle_redis_error`

### GET Request
Returns file metadata as JSON (for debugging/API).

### POST Request
```
POST /verify/<token>
Content-Type: application/x-www-form-urlencoded

password=<user_input>
```

### Flow
```
1. Get metadata
2. If no password provided → error
3. Verify password against stored hash
4. If CORRECT:
   - Reset attempt counter
   - Call serve_and_delete() → download
5. If WRONG:
   - Increment attempt counter
   - If max retries reached → lock (403)
   - Else → show error with remaining attempts
```

### Security
- Max 5 attempts before lock
- Does NOT delete file on lock (prevents DoS)
- Counter persisted in Redis

### Connections
- Called from: `password.html` form
- On success: `serve_and_delete()` streams file

---

## 📖 6. `/list-files`

**Method**: GET  
**Auth**: Admin Required 🔐  
**Decorator**: `@admin_required`, `@handle_redis_error`

### Response
Renders `admin/list_files.html` with anonymized file list.

### Data Shown
- Token (ID)
- Content type
- Protected status

### NOT Shown (Zero-Knowledge)
- Original filename
- Password hash
- Encryption keys

---

## 📖 7. `/info/<token>`

**Method**: GET  
**Auth**: Admin Required 🔐

### Response
```json
{
  "status": "success",
  "metadata": { ... }
}
```

### Purpose
API endpoint to get full metadata for a file.

---

## 📖 8. `/stats`

**Method**: GET  
**Auth**: Admin Required 🔐

### Response
Renders `stats.html` dashboard with:
- Total uploads
- Total downloads
- Page visits
- Protected vs unprotected counts

---

## 📖 9. `/stats-json`

**Method**: GET  
**Auth**: None (but just counters)  
**Decorator**: `@handle_redis_error`

### Response
```json
{
  "uploads": 42,
  "downloads": 38,
  "deletions": 35,
  "index_visits": 150,
  ...
}
```

### Purpose
AJAX endpoint for real-time stats updates.

---

## 📖 10. `/error/<code>`

**Method**: GET  
**Auth**: None

### Purpose
Renders error page for given HTTP status code.

### Supported Codes
- 400, 401, 403, 404, 410, 500, 503, 504

### Usage
JavaScript can redirect here: `window.location = '/error/404'`

---

## 🔧 Helper Functions

### `handle_redis_error` Decorator

Wraps routes to catch Redis errors:
- ConnectionError → 503
- TimeoutError → 504
- WatchError → 500
- Generic RedisError → 500

### `serve_and_delete()`

Located in `app/utils/serve_and_delete.py`

Purpose:
1. Decrypt file (if encrypted)
2. Stream to user
3. Delete file from disk
4. Delete metadata from Redis

---

## 🔐 Auth Flow

```
                    ┌─────────────┐
                    │   Request   │
                    └──────┬──────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Has @admin_required?│
                └──────────┬──────────┘
                     │           │
                    NO          YES
                     │           │
                     ▼           ▼
              ┌──────────┐ ┌─────────────┐
              │ Process  │ │ Logged in?  │
              │ normally │ └──────┬──────┘
              └──────────┘   │          │
                            NO         YES
                             │          │
                             ▼          ▼
                      ┌──────────┐ ┌──────────┐
                      │ Redirect │ │ Process  │
                      │ to login │ │ route    │
                      └──────────┘ └──────────┘
```

Admin routes protected by `@admin_required` decorator.

---

## 📊 Counter Tracking

| Counter                 | Incremented When                |
| ----------------------- | ------------------------------- |
| `index_visits`          | Home page loaded                |
| `uploads`               | File uploaded successfully      |
| `downloads`             | File downloaded successfully    |
| `protected_downloads`   | Protected file download started |
| `unprotected_downloads` | Unprotected file downloaded     |
| `list_files_visits`     | Admin views file list           |
| `info_visits`           | Admin views file info           |
