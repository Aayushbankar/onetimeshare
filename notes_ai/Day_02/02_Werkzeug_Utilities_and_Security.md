# 02. Werkzeug Utilities & Filename Security

## The Problem: Trusting User Input

Recall from the previous note: `file.filename` comes directly from the user. Let's see why this is dangerous.

### Path Traversal Attack (Directory Traversal)

Imagine your upload code does this:
```python
filepath = f"uploads/{file.filename}"
file.save(filepath)
```

A malicious user could set their filename to `../../../etc/cron.d/evil_job`. The resulting path would be:
```
uploads/../../../etc/cron.d/evil_job
```
Which resolves to `/etc/cron.d/evil_job` — they've just written a file outside your uploads folder!

This is called a **Path Traversal** or **Directory Traversal** attack.

---

## First Line of Defense: `secure_filename()`

Werkzeug provides `secure_filename()` to sanitize filenames:

```python
from werkzeug.utils import secure_filename

filename = secure_filename("../../../etc/passwd")
# Returns: "etc_passwd"

filename = secure_filename("My Résumé (2025).pdf")
# Returns: "My_Resume_2025.pdf"
```

### What It Does
1. **Strips path separators**: Removes `/` and `\`.
2. **Removes dangerous characters**: Only keeps alphanumerics, underscores, hyphens, and dots.
3. **Normalizes unicode**: Converts `é` → `e`.
4. **Handles edge cases**: Returns empty string for fully malicious names.

### Example Usage
```python
from werkzeug.utils import secure_filename

@bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    # Sanitize the filename
    safe_name = secure_filename(file.filename)
    
    if safe_name == '':
        return jsonify({"error": "Invalid filename"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(filepath)
```

---

## Why `secure_filename()` Isn't Enough

While `secure_filename()` prevents path traversal, it doesn't solve:

1. **Filename Collisions**
   - Two users upload `report.pdf` → Second one overwrites the first!

2. **Predictable Names**
   - Attacker can guess other users' files: `/uploads/report.pdf`, `/uploads/invoice.pdf`...

3. **Filename Leakage**
   - Original filename might contain sensitive info: `medical_records_john_smith.pdf`

---

## Second Line of Defense: UUIDs

Instead of using the original filename at all, we generate a **Universally Unique Identifier (UUID)**.

```python
import uuid

unique_id = str(uuid.uuid4())
# Returns something like: "550e8400-e29b-41d4-a716-446655440000"
```

### The Ultimate Secure Upload Pattern

```python
import os
import uuid
from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'

@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Generate a unique ID - this becomes the "token" for the file
    unique_id = str(uuid.uuid4())
    
    # Optionally preserve the file extension
    original_ext = os.path.splitext(file.filename)[1]  # e.g., ".pdf"
    stored_filename = f"{unique_id}{original_ext}"
    
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save with the unique filename
    filepath = os.path.join(UPLOAD_FOLDER, stored_filename)
    file.save(filepath)
    
    return jsonify({
        "id": unique_id,
        "status": "uploaded"
    }), 201
```

### Benefits
1. **No Collisions**: UUID4 has 2^122 possible values — collision is practically impossible.
2. **Unpredictable**: No one can guess other users' file IDs.
3. **No Information Leakage**: The stored filename reveals nothing about the content.

---

## `os.path` Functions You Need

| Function                 | Purpose                     | Example                                                       |
| ------------------------ | --------------------------- | ------------------------------------------------------------- |
| `os.path.join(a, b)`     | Safely join path components | `os.path.join("uploads", "file.pdf")` → `"uploads/file.pdf"`  |
| `os.path.splitext(name)` | Split name and extension    | `os.path.splitext("report.pdf")` → `("report", ".pdf")`       |
| `os.path.basename(path)` | Get filename from path      | `os.path.basename("/var/uploads/file.pdf")` → `"file.pdf"`    |
| `os.path.dirname(path)`  | Get directory from path     | `os.path.dirname("/var/uploads/file.pdf")` → `"/var/uploads"` |
| `os.path.exists(path)`   | Check if path exists        | Returns `True` or `False`                                     |

### Why Use `os.path.join()`?
It handles OS-specific path separators:
- Linux/Mac: `/`
- Windows: `\`

```python
# Don't do this:
filepath = UPLOAD_FOLDER + "/" + filename  # Breaks on Windows!

# Do this:
filepath = os.path.join(UPLOAD_FOLDER, filename)  # Works everywhere
```

---

## Practice Exercises

1. **Extension Whitelist**: Modify the upload handler to only accept `.pdf`, `.txt`, and `.png` files.

2. **Test `secure_filename()`**: In a Python shell, test these inputs:
   ```python
   from werkzeug.utils import secure_filename
   
   print(secure_filename("../hack.py"))
   print(secure_filename("hello world.txt"))
   print(secure_filename("../../.bashrc"))
   print(secure_filename("   "))  # Just spaces
   ```

3. **Custom Token Format**: Instead of full UUIDs, generate shorter tokens:
   ```python
   import secrets
   short_token = secrets.token_urlsafe(16)  # 22 characters
   ```
