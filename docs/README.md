# Backend Documentation

**OneTimeShare Backend**  
**Last Updated**: January 10, 2026

---

## 📚 Documentation Index

| Document                                            | Description                 |
| --------------------------------------------------- | --------------------------- |
| [ROUTES.md](./architecture/ROUTES.md)               | All 12 routes with diagrams |
| [DOWNLOAD_FLOW.md](./architecture/DOWNLOAD_FLOW.md) | Download sequence diagrams  |
| [API_REFERENCE.md](./API.md)                        | Request/response formats    |

---

## 🗺️ Quick Route Map

```
PUBLIC
├── /                   → Home page (upload UI)
├── /upload             → POST file + password
├── /d/<token>          → Download entry point
├── /download/<token>   → Download page UI
├── /verify/<token>     → Password verification
├── /stats-json         → Analytics JSON
└── /error/<code>       → Error pages

ADMIN (requires login)
├── /list-files         → File list (anonymized)
├── /info/<token>       → File metadata JSON
└── /stats              → Analytics dashboard
```

---

## 🔄 Main User Flow

```
Upload:
  User → / → /upload → token returned

Download (unprotected):
  User → /d/token → file streamed → deleted

Download (protected):
  User → /d/token → password.html → /verify/token → file streamed → deleted
```

---

## 📂 File Locations

| File                            | Purpose               |
| ------------------------------- | --------------------- |
| `app/routes.py`                 | All route definitions |
| `app/utils/serve_and_delete.py` | Download + cleanup    |
| `app/utils/encryption_utils.py` | Encryption functions  |
| `app/utils/password_utils.py`   | Password hashing      |
| `app/services/redis_service.py` | Redis operations      |
| `app/auth/decorators.py`        | @admin_required       |
