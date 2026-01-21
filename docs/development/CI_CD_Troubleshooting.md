# CI/CD Troubleshooting Guide

## date: 2026-01-18
### Issue: Integration Test Failure in `test_cli_blocking.py`

**Error:**
The CI/CD pipeline failed with an `AssertionError` in `tests/integration/test_cli_blocking.py`.
```
E   assert b'Enter Password' in b'<!DOCTYPE html>...'
```

**Cause:**
The test was asserting for the presence of the string `"Enter Password"`, but the UI template (`templates/password.html`) had been updated to use the label **"PASSWORD"** and the placeholder **"Enter decryption key..."**. The text "Enter Password" was no longer present in the response HTML.

**Fix:**
Updated `tests/integration/test_cli_blocking.py` to assert for the correct string present in the current UI:
```python
- assert b"Enter Password" in browser_response.data
+ assert b"Enter decryption key..." in browser_response.data
```

**Verification:**
Run the specific test locally:
```bash
PYTHONPATH=. .venv/bin/pytest tests/integration/test_cli_blocking.py -v
```

### Issue: Deployment Timeout (Port Binding)

**Error:**
Deployment logs show the service acting as "healthy" but Render eventually times out with:
`Port scan timeout reached, failed to detect open port 10000`

**Cause:**
The `Dockerfile` command hardcoded the port to `5000` (`--bind=0.0.0.0:5000`), ignoring the `PORT` environment variable injected by Render (which defaults to `10000`).

**Fix:**
Updated `Dockerfile` to dynamically use the `PORT` variable:
```dockerfile
CMD ["sh", "-c", "gunicorn --workers=4 --threads=2 --timeout=120 --bind=0.0.0.0:${PORT:-5000} run:app"]
```

