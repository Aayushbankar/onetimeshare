# 03. UUID Generation Deep Dive

## What is a UUID?

UUID stands for **Universally Unique Identifier**. It's a 128-bit number designed to be unique across all space and time.

### The Format
```
550e8400-e29b-41d4-a716-446655440000
├──────┤ ├──┤ ├──┤ ├──┤ ├──────────┤
 8 chars  4    4    4    12 chars
```
- 32 hexadecimal characters
- Separated by 4 hyphens
- Total: 36 characters as a string

---

## UUID Versions (The Important Ones)

Python's `uuid` module supports multiple UUID versions. Understanding them helps you make the right choice.

### UUID Version 1 (Time-based)
```python
import uuid
uuid.uuid1()
# UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
```
- Based on: **Timestamp + MAC address**
- **Problem**: Reveals when and where it was created!
- **Use case**: When you need sortable, time-ordered IDs (but not for sec urity!)

### UUID Version 4 (Random) ✅ **USE THIS**
```python
import uuid
uuid.uuid4()
# UUID('550e8400-e29b-41d4-a716-446655440000')
```
- Based on: **Random numbers**
- **122 bits of randomness** (6 bits are fixed for version info)
- **Collision probability**: You'd need to generate 1 billion UUIDs per second for 85 years to have a 50% chance of one collision.
- **Use case**: Security-critical, unpredictable identifiers.

### UUID Version 5 (Name-based, SHA-1)
```python
import uuid
uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com')
# UUID('cfbff0d1-9375-5685-968c-48ce8b15ae17')
```
- Based on: **SHA-1 hash of namespace + name**
- **Deterministic**: Same input → Same output
- **Use case**: When you need consistent IDs for the same input.

---

## Why UUID4 for File Tokens?

### The Math of Collision Resistance

UUID4 has 122 random bits. That means:
- **5.3 × 10^36** possible UUIDs
- If you generate **1 million** UUIDs per second:
  - 50% collision chance after **100 trillion years**

For OneTimeShare, this means:
- Users cannot guess other users' file tokens.
- You don't need to check for duplicates before saving.

---

## Working with UUIDs in Python

### Basic Generation
```python
import uuid

# Generate a new UUID4
my_uuid = uuid.uuid4()
print(my_uuid)        # 550e8400-e29b-41d4-a716-446655440000
print(type(my_uuid))  # <class 'uuid.UUID'>
```

### Converting to String
```python
# Method 1: str()
my_uuid_str = str(uuid.uuid4())
# '550e8400-e29b-41d4-a716-446655440000'

# Method 2: .hex (no hyphens)
my_uuid_hex = uuid.uuid4().hex
# '550e8400e29b41d4a716446655440000'  (32 chars, no hyphens)
```

### Parsing a UUID String
```python
uuid_obj = uuid.UUID('550e8400-e29b-41d4-a716-446655440000')
print(uuid_obj.version)  # 4
```

---

## Alternative: `secrets` Module

For even more security-critical tokens, Python's `secrets` module (added in 3.6) is designed specifically for cryptographic use.

```python
import secrets

# URL-safe token (base64-encoded)
token = secrets.token_urlsafe(16)  # 16 bytes → 22 characters
# 'dGhpcyBpcyBhIHNlY3JldA'

# Hex token
token = secrets.token_hex(16)  # 16 bytes → 32 hex characters
# 'a3b8f4c2d1e5678901234567890abcde'
```

### UUID4 vs `secrets.token_urlsafe()`

| Feature     | UUID4            | `secrets.token_urlsafe(16)` |
| ----------- | ---------------- | --------------------------- |
| Length      | 36 chars         | 22 chars                    |
| Format      | Hyphens included | URL-safe characters         |
| Randomness  | 122 bits         | 128 bits                    |
| Readability | Standard format  | Shorter but arbitrary       |

**For OneTimeShare**: Either works! UUID4 is more standard; `secrets` is shorter.

---

## Practical: Using UUIDs in Your Upload Handler

```python
import uuid
import os
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
    
    # Generate unique token
    token = str(uuid.uuid4())
    
    # Get file extension from original filename
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()  # Normalize to lowercase
    
    # Create stored filename
    stored_filename = f"{token}{ext}"
    
    # Save the file
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(os.path.join(UPLOAD_FOLDER, stored_filename))
    
    # Return the token (this becomes the shareable link ID)
    return jsonify({
        "token": token,
        "message": "File uploaded successfully"
    }), 201
```

---

## Practice Exercises

1. **UUID Inspector**: Write a script that generates 10 UUID4s and prints their version:
   ```python
   for _ in range(10):
       u = uuid.uuid4()
       print(f"{u} - Version: {u.version}")
   ```

2. **Token Comparison**: Generate 1 million UUIDs and verify no collisions:
   ```python
   tokens = set()
   for _ in range(1_000_000):
       tokens.add(str(uuid.uuid4()))
   print(f"Unique tokens: {len(tokens)}")  # Should be 1,000,000
   ```

3. **Short Token**: Modify the upload handler to use `secrets.token_urlsafe(12)` instead of UUID4. What are the trade-offs?
