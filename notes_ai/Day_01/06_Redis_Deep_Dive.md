# 06. Redis Deep Dive & Integration

## 🧠 The Mental Model: What is Redis?

**Redis** (Remote Dictionary Server) is often called a *data structure store*.

Think of it not as a "database" (like SQL with tables and rows), but as a **giant, shared Python Dictionary** running in memory.

*   **SQL Database**: Writes to disk. Slow but detailed. Good for permanent records (Users, Invoices).
*   **Redis**: Writes to RAM. Blazingly fast. Good for temporary data (Cache, Sessions, Rate Limiting).

### Why for OneTimeShare?
We are building a *One-Time* share app. The data is **ephemeral** by design.
We want files to disappear.
*   **SQL approach**: SAVE file -> Run a cron job every hour -> DELETE if time > 24hrs. (Slow, complex).
*   **Redis approach**: SAVE file -> Set **TTL** (Time To Live) to 24hrs -> Redis deletes it automatically. (Fast, simple).

---

## 🔌 Connecting in Docker

This is where beginners get stuck.

### The "Localhost" Trap
When running locally:
```python
# Works on your laptop
r = redis.Redis(host='localhost', port=6379)
```

Inside a Docker container, `localhost` means *the container itself*. Your Flask app container does NOT have Redis inside it. Redis is in the *neighbor* container.

### The Docker Network Solution
In `docker-compose.yml`, we named our service `redis`. Docker creates a DNS entry for this.
```python
# Works inside Docker
r = redis.Redis(host='redis', port=6379)
```

---

## 🛠️ Implementation Guide regarding "What's Left"

For today's Day 01 tasks, we need to bridge Flask and Redis.

### 1. Requirements
Ensure `redis` is in your `requirements.txt`.
```text
flask
redis
gunicorn
```

### 2. The Code Changes

#### A. Initialize in Factory (`app/__init__.py`)
We need to create the connection *outside* the factory (so it's global/accessible) or *inside* and attach it. A common pattern for simple apps is global extension, initialized in factory.

**Better Pattern for Factory**:
We can check if it works simply first.

```python
# app/__init__.py
from flask import Flask
import redis
import os

# Define global variable, but don't connect yet? 
# Or just connect generally (Redis clients are lazy usually).

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # 1. Config for Redis (Defaults to 'redis' hostname for Docker)
    redis_host = os.environ.get('REDIS_HOST', 'redis')
    
    # 2. Attach Redis to the app instance so we can access it via current_app
    app.redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
```

*Note: `decode_responses=True` is crucial! Without it, Redis returns `b'strings'` (bytes). With it, you get normal Python strings.*

#### B. The Test Route (`app/routes.py`)
Now we use it.

```python
# app/routes.py
from flask import Blueprint, current_app

bp = Blueprint('main', __name__)

@bp.route('/test-redis')
def test_redis():
    # Access the client we attached to the app
    try:
        r = current_app.redis_client
        
        # 1. INCR: Atomic counter. 
        # Even if 100 people hit this at once, it counts correctly.
        hits = r.incr('hit_counter')
        
        return f"Hello! This page has been seen {hits} times. Redis is ALIVE."
        
    except Exception as e:
        return f"Redis Error: {str(e)}"
```

---

## 🧪 Experiments ("The Examples")

Once you implement the above, here is how you verify it behaves like a "Textbook" system:

1.  **Persistence**: Restart the flask container. The counter should *remember* the number (because Redis container wasn't killed).
2.  **Ephemerality**: Restart the *Redis* container (without volumes). The counter resets to 1.
3.  **TTL (The Magic)**:
    ```python
    # Try this in a route
    r.set('secret', 'I will self destruct', ex=10) # ex=10 seconds
    ```
    If you Get it immediately -> "I will self destruct".
    Wait 11 seconds -> `None`.

This mechanism is the **Core Engine** of OneTimeShare.

---

## 🏃‍♂️ How to Run & Verify (The Execution Flow)

Now that you have the infrastructure, here is how you bring it to life.

### 1. The Magic Command
To start both Flask and Redis in harmony:
```bash
docker-compose up --build
```
*   `up`: Starts the containers.
*   `--build`: Recompiles your Python code/Dockerfile if you changed it.

### 2. What happens when you hit Enter?
1.  **Docker** reads `docker-compose.yml`.
2.  It sees `redis` service -> pulls `redis:alpine` -> Starts it on internal IP (e.g., 172.0.0.2).
3.  It sees `web` service -> Builds your `. ` directory -> Starts container.
4.  **Vital**: It injects `REDIS_HOST=redis` into the `web` container's environment.
5.  **Flask Starts**:
    *   `run.py` calls `create_app()`.
    *   `app/__init__.py` runs `os.environ.get('REDIS_HOST', 'localhost')` -> Gets "redis".
    *   Python resolves "redis" to the internal IP 172.0.0.2.
    *   Connection successful!

---

## 📜 Syntax Deep Dive: The Redis Boilerplate

You asked for the specific syntax. Here is the line-by-line breakdown of the "Boilerplate" you will write 100 times in your career.

### The Connection
```python
r = redis.Redis(
    host='localhost',    # The address. 'localhost' for laptop, 'redis' for docker.
    port=6379,           # The default Redis port (like 80 for web).
    db=0,                # Redis has 16 logical databases (0-15). Default is 0.
    decode_responses=True # CRITICAL. Converts bytes (b'hello') -> string ('hello').
)
```

### The Big 3 Commands
These are 90% of what you use Redis for.

#### 1. SET (Save Data)
```python
# usage: r.set(key, value, ex=seconds)
r.set('user:101:session', 'logged_in', ex=3600)
```
*   `key`: Must be unique. Use colons to namespace (e.g., `folder:file:id`).
*   `value`: The data. Strings or Integers. (For complex objects, use JSON strings).
*   `ex`: (Optional) Expire time in seconds.

#### 2. GET (Retrieve Data)
```python
value = r.get('user:101:session')
# returns: 'logged_in' or None if expired/missing.
```

#### 3. DELETE (Manual Remove)
```python
r.delete('user:101:session')
```

### Reference: The Flask Integration Pattern
In `app/__init__.py`, we attached it to `app`.
Why? So we can use it *anywhere* without reconnecting.

**In routes:**
```python
from flask import current_app
# current_app is a proxy to the active app handling the request
redis_client = current_app.redis_client 
# Now use redis_client.get(), .set(), etc.
```


---

## 💾 Where is the data stored? (Persistence Deep Dive)

You asked: *"Where is the data stored after I quit?"*

This is the most important concept in Dockerized storage.

### 1. The Default Layer (RAM)
Redis is In-Memory.
*   **While Running**: Data is in RAM.
*   **Stop Container (`docker-compose stop`)**: Data is *Usually* saved to disk inside the container (dump.rdb).
*   **Remove Container (`docker-compose down`)**: 💥 POOF. Everything is gone. The container filesystem is destroyed.

### 2. The Solution: Docker Volumes ("The Portal")
To keep data after deleting the container, we maps a folder on your **Host Machine** (Laptop) to the **Container**.

**In `docker-compose.yml` (Day 2 Preview):**
```yaml
  redis:
    image: redis:alpine
    volumes:
      - ./redis_data:/data
```
*   `./redis_data`: A folder on your laptop.
*   `/data`: The folder where Redis saves `dump.rdb`.

### 3. Redis Persistence Modes
Even with a volume, *how* does Redis save RAM to Disk?
1.  **RDB (Snapshots)**: Default. Saves every X minutes. Good for backups. (e.g., "Save if 1 key changed in 5 min").
2.  **AOF (Append Only File)**: Logs every write command. Slower but safer.

**For OneTimeShare**:
We actually **DON'T** care much about complex persistence because our data is *supposed* to be deleted! But we will use a Volume just so you don't lose data while developing.
