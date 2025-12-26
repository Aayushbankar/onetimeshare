# 📅 Day 1: Skeleton & Prototype
**Date**: December 25, 2025
**Focus**: Flask App Structure, Docker Environment, Basic Connectivity

---

## 🎯 Daily Goals
By the end of today, you should have:
1.  **A Clean Project Structure**: organized following Python best practices.
2.  **Running Containers**: Flask and Redis running via Docker Compose.
3.  **Proof of Life**: A browser visiting `localhost:5000` sees "OneTimeShare is running!".
4.  **Connectivity**: The Flask app can successfully set and get a value from Redis.
5.  **Basic Upload**: A simple API endpoint that accepts a POST request.

---

## 📋 Task List

### 1. Flask Application Setup
- [x] Create `requirements.txt` with initial dependencies:
  - `flask`
  - `redis`
  - `gunicorn` (good practice to have, even if using dev server initially)
- [x] Implement **Application Factory Pattern** in `app/__init__.py`.
- [x] Create the entry point `run.py`.
- [x] Create a "Hello World" route to test the server.

### 2. Docker Setup
- [x] Write a `Dockerfile` for the Python application:
  - Use a lightweight base image (e.g., `python:3.11-slim`).
  - Set work directory and install requirements.
- [x] Write `docker-compose.yml`:
  - Service `web`: Builds from current dir, maps port 5000.
  - Service `redis`: Uses official `redis:alpine` image.
  - Define a network so they can talk to each other.

### 3. Redis Integration
- [x] Initialize Redis client in `app/__init__.py`.
- [x] Create a test route `/test-redis` that increments a counter in Redis and returns it.

### 4. Basic Upload Endpoint
- [x] Create `app/routes.py`.
- [x] Add a POST `/upload` route.
- [x] Return a mock JSON response (e.g., `{"status": "received"}`).

---

## 🧠 Learning Objectives (To Document)

### **1. The Application Factory Pattern**
*   **Concept**: Instead of creating a global `app = Flask(__name__)`, you write a function `def create_app(): return app`.
*   **Why**: This is critical for testing and future scalability. It allows you to create multiple instances of the app with different configurations (Testing, Dev, Prod) without global state pollution.

### **2. Docker Networking**
*   **Concept**: How containers communicate.
*   **Key Takeaway**: In `docker-compose`, services can reach each other by **hostname**. Your Flask app will talk to `redis` (the service name), not `localhost` or `127.0.0.1`.
    *   *Mistake Learned*: Trying to use `localhost` inside Docker fails because it refers to the container itself.
    *   *Fix*: Used `os.environ.get('REDIS_HOST', 'localhost')` to support both modes.

### **3. Redis as Ephemeral Storage**
*   **Concept**: Redis is an in-memory key-value store.
*   **Why**: Perfect for this app because valid data is temporary. We don't need the heavy overhead of SQL schema migrations for data that deletes itself in 24 hours.

### **4. Understanding HTTP Methods (405 Error)**
*   **Concept**: Browsers send GET requests by default. APIs often expect POST.
*   **Lesson**: If you define `@bp.route('/upload', methods=['POST'])`, visiting it in a browser gives `405 Method Not Allowed`.
*   **Fix**: Used `curl -X POST` to test the API correctly.

---

## 📝 Documentation Requirements
*For your daily public post / log:*

1.  **Snippet**: `docker-compose.yml`
    ```yaml
    services:
      web:
        build: .
        ports:
          - "5000:5000"
        environment:
          - REDIS_HOST=redis
        depends_on:
          - redis
      redis:
        image: redis:alpine
        ports:
          - "6379:6379"
    ```

2.  **Output**: Connect Proof
    ```text
    web-1    | 172.19.0.1 - - [25/Dec/2025 10:00:03] "GET /test-redis HTTP/1.1" 200 -
    Response: "Hello! This page has been seen 1 times. Redis is ALIVE."
    ```

3.  **Insight**: 
    > "I got stuck on the `ModuleNotFoundError` because of Python's relative imports inside packages. I learned that `from . import routes` is required inside a package like `app`. Also, `localhost` inside Docker is a trap! It points to the container, not my computer."

4.  **Command**: The one magic command to start everything:
    `docker-compose up --build`
