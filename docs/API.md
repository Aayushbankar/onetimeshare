# OneTimeShare API Documentation

> **Version**: v1.0.0  
> **Base URL**: `https://onetimeshare.onrender.com` (or `http://localhost:5000` locally)

---

## Overview

OneTimeShare provides a REST API for secure, one-time file sharing. Files are encrypted at rest and automatically deleted after download.

### Authentication
- **Public Endpoints**: Upload, download, stats
- **Admin Endpoints**: Require session auth or JWT token
- **Rate Limits**: 5 uploads/hour, 60 downloads/minute

---

## Public Endpoints

### Health Check
```http
GET /health
```

**Response**: `200 OK`
```json
{ "status": "healthy" }
```

---

### Upload File
```http
POST /upload
Content-Type: multipart/form-data
```

**Rate Limit**: 5 per hour

**Parameters**:
| Field      | Type   | Required | Description                      |
| ---------- | ------ | -------- | -------------------------------- |
| `file`     | File   | Yes      | File to upload (max 20MB)        |
| `password` | String | No       | Optional password for encryption |

**Response**: `201 Created`
```json
{
  "status": "success",
  "metadata": {
    "token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.txt",
    "filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.txt",
    "real_filename": "secret.txt",
    "content_type": "text/plain",
    "is_protected": "True",
    "is_encrypted": "True"
  }
}
```

**Errors**:
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Upload failed

---

### Download File
```http
GET /d/<token>
```

**Rate Limit**: 60 per minute

**Behavior**:
- **Unprotected files**: Immediately serves and deletes
- **Protected files**: Redirects to password page
- **CLI tools (curl/wget)**: Returns `406 Not Acceptable`

**Response** (unprotected): File download with `Content-Disposition: attachment`

**Response** (protected): HTML password form

**Errors**:
- `406 Not Acceptable` - CLI access blocked
- `410 Gone` - File already downloaded or expired
- `403 Forbidden` - Max password attempts exceeded

---

### Verify Password
```http
POST /verify/<token>
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
| Field      | Type   | Required | Description         |
| ---------- | ------ | -------- | ------------------- |
| `password` | String | Yes      | Decryption password |

**Response** (success): File download

**Response** (failure): Redirect to password page with error

**Notes**: 
- Maximum 5 attempts before lockout
- Locked files cannot be accessed

---

### Get Stats (Public)
```http
GET /stats-json
```

**Response**: `200 OK`
```json
{
  "uploads": 42,
  "protected_downloads": 15,
  "unprotected_downloads": 27,
  "deletions": 40,
  "failed_validations": 3,
  "expired_files": 5,
  "limit_hits": 2,
  "info_visits": 10
}
```

---

## Admin Endpoints

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
| Field      | Type   | Required |
| ---------- | ------ | -------- |
| `username` | String | Yes      |
| `password` | String | Yes      |

**Response**: Redirect to dashboard on success

---

### Get JWT Token
```http
POST /auth/api/token
Content-Type: application/json
```

**Request Body**:
```json
{
  "username": "admin",
  "password": "your-password"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### File Info (Admin)
```http
GET /info/<token>
Authorization: Bearer <jwt-token>
```

**Response**: `200 OK`
```json
{
  "status": "success",
  "metadata": {
    "filename": "a1b2c3d4.txt",
    "real_filename": "secret.txt",
    "content_type": "text/plain",
    "upload_time": "2026-01-20T12:00:00",
    "is_protected": "True"
  }
}
```

---

### List Files (Admin)
```http
GET /admin/files
```
*Requires session authentication*

**Response**: HTML page with anonymized file list

---

## Error Responses

All errors follow this format:
```json
{
  "status": "error",
  "error": "Error message here"
}
```

| Code  | Meaning                        |
| ----- | ------------------------------ |
| `400` | Bad request                    |
| `401` | Unauthorized                   |
| `403` | Forbidden (locked/max retries) |
| `406` | CLI access blocked             |
| `410` | File expired/deleted           |
| `429` | Rate limit exceeded            |
| `500` | Server error                   |
| `503` | Redis unavailable              |

---

## Rate Limits

| Endpoint         | Limit         |
| ---------------- | ------------- |
| `POST /upload`   | 5 per hour    |
| `GET /d/<token>` | 60 per minute |

When rate limited, response includes:
```
Retry-After: 3600
```

---

## Encryption

- **Algorithm**: ChaCha20-Poly1305
- **Key Derivation**: Argon2id (for password-protected files)
- **Chunk Size**: 64KB (streaming encryption)

Password-protected files use zero-knowledge encryption — the server never stores the plaintext password.
