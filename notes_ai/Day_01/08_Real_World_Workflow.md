# 08. Real World Developer Workflow

How do developers actually use Docker? Do we run `docker build` every time we change a line of code? **No.**

## 1. Local Development: `docker-compose`
Running raw `docker run` commands is tedious (mapping ports, setting env vars manually).
We use **Docker Compose**. It's a file (`docker-compose.yml`) that defines your stack.

### The Problem: "Rebuild Hell"
If you put your code inside the image, you have to rebuild the image every time you save a file. That is too slow for coding.

### The Solution: Volumes (Bind Mounts)
We "map" a folder on our host machine to a folder inside the container.
```yaml
services:
  web:
    build: .
    volumes:
      - .:/app  # <--- MAGIC!
```
Now, when you edit `app/routes.py` in VS Code, the container sees the change immediately.
Combined with Flask's debug mode (reloader), the server restarts automatically inside the container.

## 2. Networking (Redis & Databases)
You plan to use Redis.
- **Without Docker**: You install Redis on your Mac/Linux. You run `service redis start`. It runs on `localhost:6379`.
- **With Docker**: Redis runs in its own container.
    - Your Flask app cannot reach it at `localhost` (because `localhost` inside the Flask container means *the Flask container itself*).
    - **Service Discovery**: Docker Compose creates a network. You access Redis by its service name.
    ```python
    # In Flask config
    REDIS_HOST = 'redis_service_name' # Not 'localhost'
    ```

## 3. The Modern Stack Workflow
1.  **Write Code** on host (VS Code).
2.  **Run Stack**: `docker-compose up` (Runs Flask + Redis).
3.  **Files Sync** via Volumes.
4.  **Logs** stream to your terminal.
5.  **Ctrl+C** stops everything cleanly.

This ensures that what you are running is identical to what your teammates run, and very close to what runs in production.
