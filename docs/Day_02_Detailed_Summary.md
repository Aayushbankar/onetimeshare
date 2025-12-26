# 📔 Developer Diary: Day 02 - The Core Logic Battle

**Date**: December 26, 2025
**Time**: 12:00 PM to 3:30 PM
**Mood**: Confident → Confused → Frustrated → Determined → **Victorious**

---

## 12:00 PM - The Plan
Day 1 was about the skeleton. Day 2 is about making it *do* something.
The goal: Accept a file upload, give it a unique ID, save it to disk, and store metadata in Redis.
Sounds simple. It wasn't.

*   Read through the learning notes I created earlier.
*   Understood the concepts: FileStorage, UUIDs, Redis Hashes.
*   Felt ready. I was wrong.

## 12:30 PM - The Configuration Trap

I started by creating a proper `config.py` file. Environment variables, defaults, the whole thing.
```python
class Config:
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif','env'}.
```

**The Mistake:** Do you see it? There's a period at the end of the set.
I didn't notice it for 20 minutes.
Python gave me a syntax error, and I kept looking at the wrong line.
*Lesson:* Always run `python -c "import config"` after editing config files. Syntax errors hide in plain sight.

## 12:45 PM - The Import Shadowing Disaster

In `utils.py`, I wrote:
```python
import config

def upload_and_store(filename):
    config = Config()  # Wait... what?
```

**The Crash:** `NameError: name 'Config' is not defined`.

*My thought process:* "But I imported it!"

*The Revelation:* I imported the **module** called `config`, not the **class** called `Config` inside it. Then I tried to use `Config()` which doesn't exist. AND I shadowed the module with a local variable named `config`.

This is like ordering a pizza box and wondering where the pizza is.

*The Fix:*
```python
from config import Config  # Import the CLASS directly
```

## 01:15 PM - The "It Works, But It Doesn't" Phase

I got the upload endpoint working... kind of.
I could POST a file. I got a 201 response. But something was wrong.

I checked the `uploads/` folder.
**It was empty.**

*The Investigation:* I had commented out `file.save(filepath)` while debugging earlier and forgot to uncomment it.

*The Crime:* My API returned `"status": "success"` for an operation that never happened.

*The Lesson:* **Never return success for operations that didn't happen.** This is how production bugs are born.

## 01:45 PM - Docker Networking (Again!)

I ran the container. I hit `/test-redis`.
```
Redis Error: Error -2 connecting to redis:6379. Name or service not known.
```

*The Confusion:* "But it worked yesterday!"

*The Realization:* Yesterday I ran it inside Docker. Today I ran Flask locally with `python run.py`. On my machine, `redis` is not a valid hostname. Only inside Docker's network does `redis` resolve to the Redis container.

*The Fix:* I added `REDIS_HOST=redis` to `docker-compose.yml`'s `web` service environment. With the default fallback to `localhost` in config.py, it works both ways now.

## 02:15 PM - The Try 3 Disaster (The Missing Folder)

I added extension validation. I added file size checks. I added Redis metadata storage with TTL.
I was proud.

I tested it:
```json
{"error": "[Errno 2] No such file or directory: 'uploads/abc123.txt'"}
```

**The Face-Palm Moment:** I had *deleted* the `os.makedirs()` line while refactoring.

*The Irony:* In my notes, I literally wrote "Ensure the upload folder is created if it doesn't exist." I then proceeded to remove the code that does exactly that.

*The Fix:* Added `os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)` back.

## 02:45 PM - The decode_responses Gotcha

Finally, uploads were working! Time to test `/info/<token>`.
The response:
```python
{b'filename': b'abc123.txt', b'content_type': b'text/plain'}
```

*The Problem:* Those `b'...'` prefixes mean the data is bytes, not strings. My JSON serialization was broken.

*The Root Cause:* I created a new Redis connection without `decode_responses=True`.
```python
redis_client = redis.Redis(host=..., port=..., db=0)  # Missing!
```

*The Fix:*
```python
redis_client = redis.Redis(..., decode_responses=True)
```

## 03:15 PM - Victory (Try 4)

```bash
curl -X POST http://localhost:5000/upload -F "file=@test.txt"
```
```json
{
  "status": "success",
  "filename": "5872fbb3-564a-4c18-be92-5b02e979d9f8.txt",
  "token": "5872fbb3-564a-4c18-be92-5b02e979d9f8.txt"
}
```

```bash
curl http://localhost:5000/info/5872fbb3-564a-4c18-be92-5b02e979d9f8.txt
```
```json
{
  "filename": "5872fbb3-564a-4c18-be92-5b02e979d9f8.txt",
  "content_type": "text/plain",
  "upload_time": "2025-12-26T09:52:00.123456"
}
```

**It works.** Files are saved. Metadata is in Redis. TTL is set. Extension validation is active.

I exhaled for the first time in 3 hours.

---

## 📊 The Numbers

| Metric             | Value      |
| ------------------ | ---------- |
| Total Tries        | 4          |
| Starting Score     | 58%        |
| Final Score        | 95%        |
| Improvement        | +37%       |
| Time Spent         | ~3.5 hours |
| Errors Encountered | 7 major    |
| Lessons Learned    | Countless  |

---

## 🧠 Summary of Learnings

1. **Import Syntax**: `import module` ≠ `from module import Class`. Know the difference cold.

2. **Variable Shadowing**: If you name a local variable the same as an import, Python won't warn you. It'll just break.

3. **Don't Lie to Your Users**: If `file.save()` is commented out, don't return `"success": true`.

4. **os.makedirs() is Not Optional**: Before writing to a folder, make sure it exists. Every. Single. Time.

5. **decode_responses=True**: Always use this with Redis in Python unless you have a specific reason not to.

6. **Docker Networking (Again)**: `localhost` means different things depending on where you are. Inside Docker, use service names.

7. **Commented Code is Dangerous**: If you're debugging, use print statements or a debugger. Don't comment out critical operations.

---

## 💭 Personal Reflection

This was harder than Day 1. Not because the concepts were harder, but because *integration* is harder than *understanding*.

I understood each piece:
- How Flask handles uploads
- How UUIDs work
- How Redis hashes work
- How config files work

But putting them together? That's where the real learning happened.

The AI professor was right: *"Integration is harder than understanding. You understand each piece — now you need to build the muscle memory of connecting them."*

Today I built that muscle memory by making every possible mistake and fixing them one by one.

Tomorrow is Day 3: Link Generation & Download Endpoint.

I'm exhausted. But I'm ready.

---

**Final Mood**: Tired, but proud. 🏆
