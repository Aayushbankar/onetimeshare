# 📔 Developer Diary: Day 01 - The Genesis of OneTimeShare

**Date**: December 25, 2025
**Time**: Morning to Afternoon
**Mood**: Excited -> Frustrated -> Enlightened -> Triumphant

---

## 09:00 AM - The Setup
I started with a blank slate. The goal was simple: get a Flask app talking to Redis inside Docker.
I created the directory structure. I felt confident.
*   Created `app/` folder.
*   Created `run.py`.
*   Created `Dockerfile`.

## 09:30 AM - The First Stumble (The Application Factory)
I tried to set up Flask. I vaguely remembered that "Global Variables are bad", so I decided to use the **Application Factory Pattern**.
I wrote `def create_app():` in `app/__init__.py`.

** The Mistake:**
In `run.py`, I instinctively typed:
```python
from app import app
```
I tried to run it.
**CRASH.** `ImportError`.
*My thought process:* "Why? It's right there!"
*Realization:* `app/__init__.py` has a *function* called `create_app`, not a variable called `app`. I was mixing up the "Simple Tutorial" style with the "Professional" style.
*Correction:* Changed `run.py` to call the factory: `app = create_app()`.

## 10:15 AM - The Phantom File (`app.py`)
I created an empty file named `app/app.py` just in case I needed it.
**Big Mistake.**
Python got confused. It saw `app` folder and `app.py` file and didn't know which one was the package.
*Action:* I deleted `app/app.py` immediately to force Python to use `__init__.py`.

## 11:00 AM - The Relative Import Nightmare
I tried to organize my routes. I put them in `app/routes.py`.
In `app/__init__.py`, I simply added `import routes`.
**CRASH.**
```text
ModuleNotFoundError: No module named 'routes'
```
*Confusion:* "But it's right next to it!"
*The Deep Dive:* I learned that in Python 3, inside a package, you *cannot* use implicit relative imports. You have to be explicit.
*The Fix:* Changed it to `from . import routes`. The dot `.` means "look in the current directory".

## 12:00 PM - Enter Docker (The Localhost Trap)
I set up `docker-compose.yml`.
I needed to connect Flask to Redis.
```python
# My first attempt
redis_client = redis.Redis(host='localhost', port=6379)
```
I ran `docker-compose up`.
**Error:** `ConnectionRefused`.
*The realization:* `localhost` inside a container means "This Container". My Flask container tried to find Redis inside itself. It wasn't there. Redis was in the *other* container.
*The Fix:* I learned about Docker DNS. I had to use the service name.
```python
# The fix
redis_host = os.environ.get('REDIS_HOST', 'redis')
```

## 01:30 PM - The "Method Not Allowed" (405)
Everything was running! I was so happy.
I went to my browser: `http://localhost:5000/upload`.
**Error:** `405 Method Not Allowed`.
I sat there staring at the screen. "But I defined the route!"
*The Code:* `@bp.route('/upload', methods=['POST'])`.
*The Epiphany:* Browsers send **GET** requests when you type in the URL bar. My code only allowed **POST**.
*The Solution:* I switched to using `curl -X POST` in the terminal to test it properly.

## 02:45 PM - Redis Persistence (The "Where did it go?" moment)
I realized that if I restart Docker, my Redis data disappears.
I learned about **Volumes**.
If I don't map a volume, Redis only saves to RAM (or a temporary disk inside the container).
*Action:* I added a volume mapping in `docker-compose.yml` so my data survives a restart.

## 03:00 PM - Victory
I ran the magic command:
```bash
docker-compose up --build
```
I saw the logs:
```text
web-1 | "GET /test-redis HTTP/1.1" 200 -
Response: "Hello! This page has been seen 1 times. Redis is ALIVE."
```
It works. The skeleton is alive.

## Summary of Learnings
1.  **Factory Pattern**: Essential for testing, but changes how `run.py` looks.
2.  **Imports**: `from . import x` is mandatory inside packages.
3.  **Docker Networking**: Service names are hostnames. `localhost` is a lie inside Docker.
4.  **HTTP**: Browsers = GET. APIs = POST. Know the difference.
5.  **Redis**: It deletes everything unless you tell it not to (TTL) or map a volume.
