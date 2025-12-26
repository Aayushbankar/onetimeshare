# 04. Redis Hashes for Metadata

## The Problem: Storing Structured Data

When a user uploads a file, we need to store more than just the file itself:
- **Original filename** (to display when downloading)
- **MIME type** (to set correct `Content-Type` header)
- **Upload timestamp** (for logging/debugging)
- **File size** (for display and validation)

We could store this as a serialized JSON string, but Redis has a better solution: **Hashes**.

---

## Redis Data Structures Review

Redis isn't just a key-value store. It supports multiple data structures:

| Type           | Description            | Use Case                           |
| -------------- | ---------------------- | ---------------------------------- |
| **String**     | Simple key-value       | Counters, simple values            |
| **Hash**       | Dictionary/Map         | Structured objects (our metadata!) |
| **List**       | Ordered collection     | Queues, timelines                  |
| **Set**        | Unordered unique items | Tags, unique visitors              |
| **Sorted Set** | Set with scores        | Leaderboards, ranked data          |

---

## Redis Hashes: A Deep Dive

A **Hash** in Redis is like a Python dictionary. It maps string fields to string values.

### Visualization
```
KEY: "file:abc123"
┌───────────────────────────────────────┐
│  HASH FIELDS                          │
├───────────────────┬───────────────────┤
│  original_name    │  "report.pdf"     │
│  content_type     │  "application/pdf"│
│  upload_time      │  "2025-12-26..."  │
│  file_size        │  "1048576"        │
└───────────────────┴───────────────────┘
```

### Why Hashes Over JSON Strings?

**JSON String Approach:**
```python
# Storing
data = json.dumps({"name": "report.pdf", "size": 1024})
redis_client.set("file:abc123", data)

# Retrieving (must parse entire JSON)
data = json.loads(redis_client.get("file:abc123"))
name = data["name"]
```

**Hash Approach:**
```python
# Storing
redis_client.hset("file:abc123", mapping={
    "name": "report.pdf",
    "size": 1024
})

# Retrieving (can get individual fields!)
name = redis_client.hget("file:abc123", "name")
```

### Advantages of Hashes
1. **Atomic field updates**: Change one field without rewriting the whole object.
2. **Memory efficient**: Redis optimizes small hashes.
3. **Fetch specific fields**: Don't load data you don't need.

---

## Redis Hash Commands

### Setting Values

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set a single field
r.hset("file:abc123", "original_name", "report.pdf")

# Set multiple fields at once (most common)
r.hset("file:abc123", mapping={
    "original_name": "report.pdf",
    "content_type": "application/pdf",
    "upload_time": "2025-12-26T10:30:00",
    "file_size": "1048576"
})
```

### Getting Values

```python
# Get a single field
name = r.hget("file:abc123", "original_name")
# Returns: "report.pdf"

# Get multiple specific fields
fields = r.hmget("file:abc123", ["original_name", "file_size"])
# Returns: ["report.pdf", "1048576"]

# Get ALL fields (returns a dictionary)
all_data = r.hgetall("file:abc123")
# Returns: {
#     "original_name": "report.pdf",
#     "content_type": "application/pdf",
#     "upload_time": "2025-12-26T10:30:00",
#     "file_size": "1048576"
# }
```

### Checking & Deleting

```python
# Check if a key exists
exists = r.exists("file:abc123")
# Returns: 1 (exists) or 0 (doesn't exist)

# Check if a field exists within a hash
has_name = r.hexists("file:abc123", "original_name")
# Returns: True or False

# Delete a field from a hash
r.hdel("file:abc123", "upload_time")

# Delete the entire key
r.delete("file:abc123")
```

---

## Designing the OneTimeShare Metadata Schema

### Key Naming Convention
Use a consistent prefix + unique ID pattern:
```
file:{uuid}
```
Example: `file:550e8400-e29b-41d4-a716-446655440000`

### Schema Definition
| Field               | Type                | Description              |
| ------------------- | ------------------- | ------------------------ |
| `original_filename` | String              | The file's original name |
| `stored_filename`   | String              | UUID-based name on disk  |
| `content_type`      | String              | MIME type                |
| `file_size`         | Integer (as string) | Size in bytes            |
| `upload_time`       | ISO 8601 String     | When uploaded            |

### Implementation

```python
import uuid
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
import redis

bp = Blueprint('main', __name__)

def get_redis():
    """Get Redis connection from app config."""
    return redis.Redis(
        host=current_app.config.get('REDIS_HOST', 'localhost'),
        port=current_app.config.get('REDIS_PORT', 6379),
        decode_responses=True
    )

@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Generate unique token
    token = str(uuid.uuid4())
    
    # Get file extension
    _, ext = os.path.splitext(file.filename)
    stored_filename = f"{token}{ext.lower()}"
    
    # Calculate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Seek back to start
    
    # Save file to disk
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, stored_filename))
    
    # Store metadata in Redis
    r = get_redis()
    r.hset(f"file:{token}", mapping={
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
```

---

## Setting TTL (Time To Live)

For OneTimeShare, files should expire. Redis can automatically delete keys after a set time:

```python
# Set expiry when storing
r.hset(f"file:{token}", mapping={...})
r.expire(f"file:{token}", 86400)  # 86400 seconds = 24 hours

# Or in one transaction using a pipeline
pipe = r.pipeline()
pipe.hset(f"file:{token}", mapping={...})
pipe.expire(f"file:{token}", 86400)
pipe.execute()
```

### Checking Remaining TTL
```python
remaining = r.ttl(f"file:{token}")
# Returns: seconds remaining, -1 if no expiry, -2 if key doesn't exist
```

---

## Practice Exercises

1. **Redis CLI Practice**: Open `redis-cli` and manually create a hash:
   ```bash
   redis-cli
   > HSET file:test001 original_filename "test.pdf" content_type "application/pdf"
   > HGETALL file:test001
   > HGET file:test001 original_filename
   > DEL file:test001
   ```

2. **Retrieve Endpoint**: Create a GET `/info/<token>` endpoint that retrieves and returns the metadata for a given token.

3. **TTL Display**: Modify the `/info/<token>` endpoint to also return how many seconds are left before the file expires.
