# 🚀 Day 30: I Shipped v1.0.0 — The Grand Finale

## Medium Blog Post

---

# I Built a Secure File Sharing App in 30 Days. Here's What I Learned About Security.

**TL;DR**: I spent 30 days building OneTimeShare — a self-destructing file sharing app. On the final day, a "720 degree" security audit revealed critical flaws I never expected. This is what I learned.

---

## The Mission

December 24th, 2025. I made a public commitment: build a production-ready, *secure* file sharing application in 30 days. No tutorials. No shortcuts. Just me, Flask, Redis, and an unreasonable ambition to write code that wouldn't embarrass me.

The idea was simple: upload a file, get a link, share it, and watch it **permanently delete** after one download. Like Snapchat, but for sensitive documents.

## The Tech Stack

- **Backend**: Python (Flask)
- **Database**: Redis (Ephemeral storage — perfect for self-destruct)
- **Encryption**: ChaCha20-Poly1305 (The same algorithm Signal uses)
- **Deployment**: Docker + Render

## The "720 Degree" Audit

On Day 30, I was ready to ship. Tests passing. Docker building. README updated.

Then I decided to do *one more pass*. A paranoid, "what would a principal engineer find?" audit.

**Finding #1: The Race Condition**

My password retry logic looked innocent:
```python
attempts = int(metadata.get('attempt_to_unlock', 0))
attempts += 1
metadata['attempt_to_unlock'] = str(attempts)
redis_service.store_file_metadata(token, metadata)
```

Spot the bug? It's a classic **Read-Modify-Write** race condition.

If an attacker sends 100 parallel requests, they could all read `attempts = 0` before any of them write `attempts = 1`. Result: unlimited password guesses.

**The Fix**: Redis `HINCRBY` — atomic increment that can't be gamed.

**Finding #2: Missing CSRF**

My admin login form had no CSRF token. Not because I forgot. Because I didn't think I needed it — "it's just a login page."

Wrong. Login CSRF is a real attack vector. An attacker could force *you* to log into *their* account, then watch your activity.

**The Fix**: Flask-WTF. 15 minutes of work. Should have been there from Day 1.

## The Lessons

1. **"Read-Modify-Write" is a Footgun**: If you're incrementing counters in a distributed system, use atomic operations. Always.

2. **Security Isn't a Checklist**: I had encryption. I had rate limiting. I still had critical vulnerabilities hiding in *logic flows*.

3. **The Final Audit Matters**: If I had shipped on Day 29, I would have released a product with a brute-force bypass. One extra day saved months of embarrassment.

## The Numbers

- **30 Days**
- **6 Critical Bugs Found (and Fixed)**
- **1 Master Project Report**
- **0 Regrets**

## Try It

🔗 **Live Demo**: [https://onetimeshare.onrender.com](https://onetimeshare.onrender.com)

📂 **Source Code**: [GitHub](https://github.com/Aayushbankar/onetimeshare)

---

*If you learned something, connect with me on LinkedIn. I document my builds in public.*

#100DaysOfCode #Python #Security #BuildInPublic

---
---
---

# Dev.to Post

---

```
---
title: "I Found a Critical Race Condition on Launch Day — Here's How I Fixed It"
published: true
description: "Day 30 of building a secure file sharing app. The final audit was brutal."
tags: python, security, flask, redis
cover_image: https://dev-to-uploads.s3.amazonaws.com/uploads/articles/placeholder.png
---
```

## 🔥 The Setup

Day 30. Final day of my 30-day build challenge. 

My app, **OneTimeShare**, was *ready*:
- ✅ End-to-end encryption (ChaCha20-Poly1305)
- ✅ Password protection with Argon2id
- ✅ Rate limiting
- ✅ Docker deployment
- ✅ 21 passing tests

I was about to push the "Release" button.

Then I decided to do *one more audit*.

## 💀 The Discovery

My password retry logic:

```python
# ❌ THE BUG
attempts = int(metadata.get('attempt_to_unlock', 0))
attempts += 1
metadata['attempt_to_unlock'] = str(attempts)
redis_service.store_file_metadata(token, metadata)
```

Can you spot it?

**It's a Read-Modify-Write race condition.**

If an attacker sends 50 parallel requests:
1. All 50 read `attempts = 0`
2. All 50 compute `attempts = 1`
3. All 50 write `attempts = 1`

Result: 50 password guesses for the price of 1.

My "5 attempt limit" was meaningless.

## ✅ The Fix

Redis has atomic operations for exactly this reason:

```python
# ✅ THE FIX
def increment_file_attempt(self, token: str) -> int:
    return self.redis_client.hincrby(token, "attempt_to_unlock", 1)
```

`HINCRBY` is atomic. It reads, increments, and writes in a single operation. No race condition possible.

## 🧠 The Lesson

> Security isn't about having the right *features*. It's about having the right *operations*.

I had encryption. I had hashing. I had rate limiting.

I still had a **logic flaw** that bypassed all of it.

## 📊 Final Stats

| Metric                       | Value |
| ---------------------------- | ----- |
| Days                         | 30    |
| Critical Bugs Found (Day 30) | 6     |
| Race Conditions              | 1     |
| Missing CSRF Tokens          | 1     |
| Coffee Cups                  | ∞     |

## 🔗 Links

- **Live Demo**: [onetimeshare.onrender.com](https://onetimeshare.onrender.com)
- **GitHub**: [github.com/Aayushbankar/onetimeshare](https://github.com/Aayushbankar/onetimeshare)
- **Security Audit Report**: In the repo under `docs/development/audit/`

---

*What's the worst bug you've found on launch day? Drop it in the comments.*

---
---
---

# LinkedIn Post (Heroic Realism Style)

---

🔥 Day 30. The finale.

I was ready to ship.

Tests passing. Docker building. README polished.

One more audit. Just to be safe.

━━━━━━━━━━━━━

THE GRAVEYARD:

🪦 My password retry logic had a race condition.
   50 parallel requests = 50 free guesses.
   My "5 attempt limit" was a lie.

🪦 My admin login had no CSRF token.
   Because "it's just a login, who cares?"
   Answer: attackers. Attackers care.

🪦 My Redis error handling leaked JSON internals.
   Nothing says "professional" like showing users
   `{"error": "Redis timeout error"}`.

━━━━━━━━━━━━━

THE RESURRECTION:

✅ Atomic Redis operations (`HINCRBY`).
   No more Read-Modify-Write footguns.

✅ Flask-WTF for CSRF protection.
   15 minutes of work. Should've done it Day 1.

✅ Proper error templates.
   Users see "503", not our shame.

━━━━━━━━━━━━━

THE INSIGHT:

Security isn't a checklist.

I had encryption (ChaCha20-Poly1305).
I had hashing (Argon2id).
I had rate limiting.

I still had critical vulnerabilities.

Because security lives in the *logic flows*.
Not just the cryptographic primitives.

━━━━━━━━━━━━━

30 days.
6 critical bugs caught on the final day.
0 regrets.

OneTimeShare v1.0.0 is live.

Link in first comment.

#BuildInPublic #Python #Security #100DaysOfCode

---
