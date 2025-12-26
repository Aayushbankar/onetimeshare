# 07. Putting It All Together

## Day 2 Complete Implementation

This is the full working implementation combining all concepts from today.

---

## Project Structure After Day 2

```
onetimeshare/
├── app/
│   ├── __init__.py      # Application factory with config
│   └── routes.py        # Upload route with validation
├── uploads/             # Created automatically
├── config.py            # Configuration classes
├── requirements.txt
├── run.py
├── Dockerfile
└── docker-compose.yml
```

---

## Updated Files

### `config.py`
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif'}
```

### `app/__init__.py`
```python
import os
from flask import Flask
import redis

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object('config.Config')
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize Redis
    app.redis = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        decode_responses=True
    )
    
    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
```

### `app/routes.py`
```python
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    return "OneTimeShare is running!"

@bp.route('/upload', methods=['POST'])
def upload():
    # Validate file presence
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Validate extension
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    # Calculate file size
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    
    # Generate unique token
    token = str(uuid.uuid4())
    
    # Get extension and create stored filename
    ext = os.path.splitext(file.filename)[1].lower()
    stored_filename = f"{token}{ext}"
    
    # Save file
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], stored_filename)
    file.save(filepath)
    
    # Store metadata in Redis
    current_app.redis.hset(f"file:{token}", mapping={
        "original_filename": file.filename,
        "stored_filename": stored_filename,
        "content_type": file.content_type or "application/octet-stream",
        "file_size": str(file_size),
        "upload_time": datetime.utcnow().isoformat()
    })
    
    return jsonify({
        "token": token,
        "message": "File uploaded successfully"
    }), 201

@bp.route('/info/<token>')
def file_info(token):
    """Get file metadata (for testing)."""
    data = current_app.redis.hgetall(f"file:{token}")
    if not data:
        return jsonify({"error": "File not found"}), 404
    return jsonify(data)
```

---

## Testing Commands

```bash
# Start the containers
docker-compose up --build

# Upload a file
curl -X POST -F "file=@test.pdf" http://localhost:5000/upload

# Check file info (replace with actual token)
curl http://localhost:5000/info/<token>
```

---

## Day 2 Checklist

- [x] File uploads save to disk with UUID filenames
- [x] Metadata stored in Redis hashes
- [x] File validation (extension, size)
- [x] Configuration via environment variables
- [x] Test route to verify metadata storage

---

## What's Next (Day 3)

Tomorrow we'll implement:
- **Link Generation**: Create shareable URLs
- **Download Endpoint**: `/d/<token>` to retrieve files
- **Database Abstraction**: Clean interface for Redis operations
