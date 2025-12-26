# 01. Flask File Uploads Deep Dive

## The Big Picture: How Files Travel Over HTTP

When you submit a form with a file, something special happens. Unlike regular form data (text fields), files are **binary blobs**. HTTP needs a special encoding to handle this.

### The Three Encodings

1. **application/x-www-form-urlencoded** (Default)
   - Used for simple forms with text fields.
   - Data looks like: `name=John&age=25`
   - Cannot handle files!

2. **multipart/form-data** (For Files)
   - Each field is sent as a separate "part".
   - Each part has headers (like `Content-Type`) and a body.
   - This is what `enctype="multipart/form-data"` does in HTML forms.

3. **application/json** (For APIs)
   - JSON-encoded data.
   - Also cannot handle raw files (you'd need to base64 encode them, which is inefficient).

### HTML Form for File Upload
```html
<form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
```
**Critical**: Without `enctype="multipart/form-data"`, only the filename is sent, not the file contents!

---

## The `request.files` Dictionary

In Flask, uploaded files are accessible via `request.files`. This is a special dictionary-like object.

```python
from flask import request

@bp.route('/upload', methods=['POST'])
def upload():
    # Access the uploaded file by its form field name
    uploaded_file = request.files['file']
```

### What is `uploaded_file`?
It's a `FileStorage` object from Werkzeug – not a regular Python file object!

---

## The FileStorage Object

`FileStorage` wraps the uploaded file and provides useful attributes and methods:

### Key Attributes
| Attribute        | Description                   | Example                  |
| ---------------- | ----------------------------- | ------------------------ |
| `filename`       | Original filename from user   | `"my_report.pdf"`        |
| `name`           | Form field name               | `"file"`                 |
| `content_type`   | MIME type                     | `"application/pdf"`      |
| `content_length` | Size in bytes (may be `None`) | `1048576`                |
| `stream`         | The file-like object          | `<SpooledTemporaryFile>` |

### Key Methods
| Method              | Description                             |
| ------------------- | --------------------------------------- |
| `save(destination)` | Save the file to disk                   |
| `read()`            | Read the file contents as bytes         |
| `seek(0)`           | Reset the file pointer to the beginning |
| `close()`           | Close the file stream                   |

### The Stream Concept
Files are stored in a **spooled temporary file**. This means:
- Small files (< 500KB by default) are kept in memory.
- Large files are written to a temp file on disk.
- You can only read the stream **once** unless you `seek(0)` back!

```python
# Wrong - reads empty bytes the second time!
data1 = uploaded_file.read()
data2 = uploaded_file.read()  # Returns b'' (empty)

# Correct - seek back to the beginning
data1 = uploaded_file.read()
uploaded_file.seek(0)
data2 = uploaded_file.read()  # Returns the full content again
```

---

## Basic File Upload Handler

```python
import os
from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'

@bp.route('/upload', methods=['POST'])
def upload():
    # 1. Check if the file key exists in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files['file']
    
    # 2. Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # 3. Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # 4. Save the file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    return jsonify({
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type
    }), 201
```

### Why Two Checks?
1. `'file' not in request.files` → User didn't include a file field at all.
2. `file.filename == ''` → File field exists but user didn't select a file.

---

## Testing with cURL

```bash
# Upload a file
curl -X POST -F "file=@/path/to/document.pdf" http://localhost:5000/upload

# -X POST: Use POST method
# -F "file=@...": Form data, @ means "read from this file path"
# The field name "file" must match request.files['file']
```

---

## ⚠️ Security Warning: Don't Trust `file.filename`!

The filename comes directly from the user's browser. A malicious user could send:
- `../../../etc/passwd` (Path Traversal Attack)
- `evil.php` (if you're running PHP alongside)
- Very long filenames (DoS)

**Never use `file.filename` directly for saving!**

We'll address this in the next note with `secure_filename()` and UUIDs.

---

## Practice Exercises

1. **Server Check**: Modify the upload handler to print the file size to the console.
   - Hint: Use `file.seek(0, 2)` to go to the end, then `file.tell()` to get position.

2. **Multiple Files**: Modify the handler to accept multiple files:
   ```python
   files = request.files.getlist('files')
   for file in files:
       # Process each file
   ```

3. **Content Type Validation**: Only accept PDF files. Return 400 for any other type.
