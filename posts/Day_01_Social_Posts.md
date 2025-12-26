# Day 01 Social Media Posts - OneTimeShare 30-Day Build Challenge

---

## 📘 LinkedIn Post (Long-Form)

**Title/Hook**: 🎄 Day 1/30: Building a One-Time Secure File Sharing App in Public

---

It's Christmas. Everyone's celebrating.
Me? I just broke my code 4 times in 6 hours. And I loved it.

I started #OneTimeShare30 — a 30-day public build challenge to create a **one-time secure file sharing app**.

**The Problem I'm Solving:**
Ever shared an API key over Slack? A password via WhatsApp? A config file via email?
That data sits on their servers. Forever.

My solution: A simple app where you upload a file → get a link → someone views it once → it's **gone forever**.

---

**Here's what actually happened on Day 1:**

🟢 **Started confident**. Created Flask skeleton, Dockerfile, docker-compose.

🔴 **First crash.** `ImportError`. I mixed "Simple Tutorial Flask" with the "Professional Factory Pattern". Took me 30 minutes to realize `app = create_app()` is different from `from app import app`.

🔴 **Second crash.** Python couldn't find my `routes.py`. Turns out, inside a Python package, you MUST use `from . import routes`. Implicit imports don't work in Python 3.

🔴 **Third crash.** Flask couldn't connect to Redis in Docker. Why? `localhost` inside a container means "THIS container", not my machine. I had to use Docker's DNS: `redis` (the service name).

🔴 **Fourth confusion.** Visited `/upload` in my browser. Got `405 Method Not Allowed`. My route only allowed POST. Browsers send GET. Switched to `curl -X POST`. It worked.

🟢 **Victory.** By 3 PM, I saw:
```
"Hello! This page has been seen 1 times. Redis is ALIVE."
```

---

**Tech Stack:**
- Python 3.11 / Flask
- Redis (for ephemeral storage — perfect for data that should disappear)
- Docker Compose

**What's Next (Day 2):**
- Secure file saving with unique IDs
- Metadata structure in Redis

---

💬 **I want YOUR input:**
- Have you built something similar? What did you use for ephemeral storage?
- Any security considerations I should think about early?

Follow along: I'm posting daily updates for 30 days.

#BuildInPublic #Python #Flask #Docker #Redis #WebDev #30DayChallenge #DeveloperLife #OneTimeShare30

---

## 🐦 X (Twitter) Thread

**Tweet 1 (Hook):**
🎄 Day 1/30 of building OneTimeShare

A one-time secure file sharing app.
You upload → Get a link → They view it → It's deleted. Forever.

Started Christmas morning. Broke my code 4 times.
Here's what happened ⬇️

---

**Tweet 2 (Problem):**
The Problem:

Ever shared an API key via Slack?
A password via WhatsApp?

That data sits on their servers. Forever.

My solution: Self-destructing file sharing.
View once → Gone.

---

**Tweet 3 (Tech):**
Tech Stack:
• Python 3.11 / Flask
• Redis (data that SHOULD disappear)
• Docker Compose

Why Redis over SQL?
Our data is ephemeral by design. Redis TTL = auto-delete. No cron jobs needed.

---

**Tweet 4 (Mistake 1):**
Mistake 1: Import Confusion

I wrote: `from app import app`
But my code had: `def create_app():`

The "Factory Pattern" vs "Tutorial Pattern" mixup.

Fix: `app = create_app()`

---

**Tweet 5 (Mistake 2):**
Mistake 2: `ModuleNotFoundError: No module named 'routes'`

I had `import routes` inside a Python package.

Python 3 rule: Use EXPLICIT relative imports.
Fix: `from . import routes`

The dot = "look in the current directory"

---

**Tweet 6 (Mistake 3):**
Mistake 3: Docker Localhost Trap

`localhost` inside a Docker container = "THIS container"

My Flask app was looking for Redis inside itself. Redis was in the OTHER container.

Fix: Use Docker DNS. Connect to `redis` (the service name).

---

**Tweet 7 (Victory):**
By 3 PM:

```
"Hello! This page has been seen 1 times. Redis is ALIVE."
```

The skeleton works. Flask + Redis + Docker. Connected.

Day 1 ✅

---

**Tweet 8 (CTA):**
Day 2 plan:
• Secure file saving
• Unique ID generation
• Redis metadata structure

💬 Your turn:
Have you built ephemeral storage before?
What did you use?

Follow along for 30 days of #BuildInPublic

#OneTimeShare30 #Python #Flask

---

## 📌 Short LinkedIn Update (Alternative - More Casual)

**🎄 Day 1/30: OneTimeShare**

Started my 30-day build challenge on Christmas.

Building a one-time secure file sharing app:
Upload → View Once → Deleted Forever.

Today's wins:
✅ Flask + Docker + Redis skeleton working
✅ Learned Docker Networking (localhost ≠ localhost inside containers!)
✅ Discovered Python 3's strict relative imports

Today's lesson:
> "localhost inside Docker is a lie. Use the service name."

Broke my code 4 times. Fixed it 4 times. That's the game.

Tomorrow: Secure file saving logic.

#BuildInPublic #Python #Flask #OneTimeShare30
