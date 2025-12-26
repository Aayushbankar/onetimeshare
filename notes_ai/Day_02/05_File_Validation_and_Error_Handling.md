# 05. File Validation & Error Handling

## Why Validation Matters

Without validation, your upload endpoint is vulnerable to:
1. **Denial of Service (DoS)**: User uploads a 10GB file, crashes your server.
2. **Storage Exhaustion**: Attackers fill your disk with junk files.
3. **Malicious Files**: Executables, scripts, or malformed files.

---

## Types of Validation

### 1. File Presence Validation
Check that a file was actually uploaded:

```python
@bp.route('/upload', methods=['POST'])
def upload():
    # Check if 'file' key exists in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files['file']
    
    # Check if the user actually selected a file
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Continue with upload...
```

### 2. File Size Validation

```python
# In your config or at the top of the file
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

def validate_file_size(file):
    """Check if file is within size limit. Returns size if valid, raises ValueError if not."""
    file.seek(0, 2)  # Seek to end of file
    size = file.tell()  # Get current position (= file size)
    file.seek(0)  # Reset to beginning
    
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes (max: {MAX_FILE_SIZE} bytes)")
    
    if size == 0:
        raise ValueError("File is empty")
    
    return size
```

### Flask-Level Size Limit
Flask also has a built-in way to reject large files early (before they're fully uploaded):

```python
# In your create_app() or config
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB
```

When exceeded, Flask raises `werkzeug.exceptions.RequestEntityTooLarge` (413 error).

### Handling the 413 Error
```python
from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    return jsonify({
        "error": "File too large",
        "max_size_mb": 10
    }), 413
```

---

### 3. File Extension Validation

```python
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

**Usage:**
```python
if not allowed_file(file.filename):
    return jsonify({
        "error": "File type not allowed",
        "allowed_types": list(ALLOWED_EXTENSIONS)
    }), 400
```

---

### 4. MIME Type Validation (Content-Type)

⚠️ **Warning**: `file.content_type` comes from the client and can be spoofed!

```python
ALLOWED_MIMETYPES = {
    'application/pdf',
    'text/plain',
    'image/png',
    'image/jpeg',
    'image/gif'
}

def validate_mimetype(file):
    """Basic MIME type check (can be spoofed!)."""
    if file.content_type not in ALLOWED_MIMETYPES:
        raise ValueError(f"MIME type {file.content_type} not allowed")
```

### Better: Magic Number Validation
Files have "magic numbers" (first few bytes) that identify their true type:

```python
# pip install python-magic
import magic

def validate_file_magic(file):
    """Check file type using magic numbers (more reliable)."""
    # Read the first 2048 bytes
    header = file.read(2048)
    file.seek(0)  # Reset file pointer
    
    mime = magic.from_buffer(header, mime=True)
    
    if mime not in ALLOWED_MIMETYPES:
        raise ValueError(f"Detected MIME type {mime} not allowed")
    
    return mime
```

---

## Comprehensive Validation Function

```python
import os

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass

def validate_uploaded_file(file):
    """
    Validate an uploaded file.
    
    Returns:
        dict with 'size' and 'extension' if valid
    
    Raises:
        FileValidationError with descriptive message if invalid
    """
    # Check 1: File exists and has a name
    if not file or file.filename == '':
        raise FileValidationError("No file selected")
    
    # Check 2: Extension allowed
    if '.' not in file.filename:
        raise FileValidationError("File must have an extension")
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"Extension '.{ext}' not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Check 3: File size
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    
    if size == 0:
        raise FileValidationError("File is empty")
    
    if size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        actual_mb = size / (1024 * 1024)
        raise FileValidationError(
            f"File too large: {actual_mb:.2f} MB (max: {max_mb:.0f} MB)"
        )
    
    return {
        "size": size,
        "extension": ext
    }
```

---

## Error Handling Patterns

### Pattern 1: Try-Except in Route
```python
@bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    
    try:
        file_info = validate_uploaded_file(file)
    except FileValidationError as e:
        return jsonify({"error": str(e)}), 400
    
    # Continue with upload...
```

### Pattern 2: Custom Error Handler
```python
from flask import jsonify

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"error": error.message}), error.status_code
```

---

## Returning Helpful Error Messages

Good error messages should be:
1. **Specific**: Tell the user exactly what's wrong.
2. **Actionable**: Tell them how to fix it.
3. **Safe**: Don't reveal internal implementation details.

### Examples

**Bad:**
```json
{"error": "Upload failed"}
{"error": "Exception in validate_file_size at line 42"}
```

**Good:**
```json
{
    "error": "File too large",
    "details": "Maximum file size is 10 MB. Your file is 15.3 MB.",
    "code": "FILE_TOO_LARGE"
}
{
    "error": "File type not allowed",
    "details": "Allowed types: pdf, txt, png, jpg, jpeg",
    "code": "INVALID_FILE_TYPE"
}
```

---

## Practice Exercises

1. **Add Error Codes**: Modify `FileValidationError` to include an error code:
   ```python
   raise FileValidationError("File too large", code="FILE_TOO_LARGE")
   ```

2. **Create a Test Script**: Write a script that tries to upload:
   - A valid PDF
   - A file that's too large (create with `dd if=/dev/zero of=large.bin bs=1M count=20`)
   - A `.exe` file (should be rejected)

3. **Rate Limiting Prep**: Research Flask-Limiter. We'll implement it later, but read about its `@limiter.limit()` decorator.
