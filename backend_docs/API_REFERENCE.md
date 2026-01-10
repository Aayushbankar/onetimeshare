# API Reference

**Base URL**: `http://localhost:5000`

---

## Public Endpoints

### POST `/upload`

Upload a file (optionally password-protected).

**Request**:
```http
POST /upload
Content-Type: multipart/form-data

file: <binary file>
password: <optional string>
```

**Response** (201 Created):
```json
{
  "status": "success",
  "metadata": {
    "filename": "abc123-def456.pdf",
    "real_filename": "document.pdf",
    "content_type": "application/pdf",
    "token": "abc123-def456",
    "is_protected": "True",
    "is_encrypted": "True"
  }
}
```

**Errors**:
| Code | Reason            |
| ---- | ----------------- |
| 400  | No file provided  |
| 500  | Upload failed     |
| 503  | Redis unavailable |

---

### GET `/d/<token>`

Download entry point. Serves file or shows password form.

**Response** (varies):
| Condition   | Response           |
| ----------- | ------------------ |
| Unprotected | Binary file stream |
| Protected   | HTML password form |
| Not found   | 410 Gone           |
| Locked      | 403 Forbidden      |

---

### POST `/verify/<token>`

Verify password and download protected file.

**Request**:
```http
POST /verify/<token>
Content-Type: application/x-www-form-urlencoded

password=mysecret
```

**Response** (varies):
| Condition | Response             |
| --------- | -------------------- |
| Correct   | Binary file stream   |
| Wrong     | HTML form with error |
| Locked    | 403 Forbidden        |

---

### GET `/stats-json`

Get analytics counters as JSON.

**Response**:
```json
{
  "uploads": 42,
  "downloads": 38,
  "deletions": 35,
  "index_visits": 150,
  "list_files_visits": 5,
  "info_visits": 3,
  "protected_downloads": 15,
  "unprotected_downloads": 23
}
```

---

## Admin Endpoints

> Requires authentication via Flask-Login session

### GET `/list-files`

List all uploaded files (anonymized).

**Response**: HTML page with file table

---

### GET `/info/<token>`

Get full metadata for a file.

**Response**:
```json
{
  "status": "success",
  "metadata": {
    "filename": "abc123.pdf",
    "real_filename": "doc.pdf",
    "content_type": "application/pdf",
    "is_protected": "True",
    "attempt_to_unlock": "2",
    ...
  }
}
```

---

### GET `/stats`

Admin dashboard with analytics.

**Response**: HTML page

---

## Error Responses

All routes may return these errors:

| Code | Body                                  | Cause         |
| ---- | ------------------------------------- | ------------- |
| 503  | `{"error": "Redis connection error"}` | Redis down    |
| 504  | `{"error": "Redis timeout error"}`    | Redis slow    |
| 500  | `{"error": "Internal server error"}`  | Unknown error |

---

## Response Headers

### On successful download:
```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="document.pdf"
Content-Length: 12345
```

### On rate limit (future):
```http
Retry-After: 3600
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
```
